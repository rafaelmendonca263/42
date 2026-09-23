/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                 +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa            #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>
#include <stdlib.h>

/* Inicialização de Recursos da Simulação */
int sim_init_resources(t_sim *sim)
{
	int i;

	sim->stop = 0;
	sim->finished_count = 0;
	if (pthread_mutex_init(&sim->print_mutex, NULL) != 0)
		return (1);
	if (pthread_mutex_init(&sim->state_mutex, NULL) != 0)
	{
		pthread_mutex_destroy(&sim->print_mutex);
		return (1);
	}

	sim->coders = malloc(sizeof(t_coder) * sim->number_of_coders);
	sim->threads = malloc(sizeof(pthread_t) * sim->number_of_coders);
	sim->dongles = malloc(sizeof(t_dongle) * sim->number_of_coders);

	if (!sim->coders || !sim->threads || !sim->dongles)
	{
		free(sim->coders);
		free(sim->threads);
		free(sim->dongles);
		pthread_mutex_destroy(&sim->print_mutex);
		pthread_mutex_destroy(&sim->state_mutex);
		return (1);
	}

	i = 0;
	while (i < sim->number_of_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].left = i;
		sim->coders[i].right = (i + 1) % sim->number_of_coders;
		sim->coders[i].last_compile_start = sim->start_ts;
		sim->coders[i].compile_count = 0;
		sim->coders[i].sim = sim;

		if (pthread_mutex_init(&sim->dongles[i].mutex, NULL) != 0)
		{
			while (--i >= 0)
			{
				pthread_mutex_destroy(&sim->dongles[i].mutex);
				pthread_cond_destroy(&sim->dongles[i].cond);
				pq_free(sim->dongles[i].queue);
			}
			free(sim->coders);
			free(sim->threads);
			free(sim->dongles);
			pthread_mutex_destroy(&sim->print_mutex);
			pthread_mutex_destroy(&sim->state_mutex);
			return (1);
		}
		if (pthread_cond_init(&sim->dongles[i].cond, NULL) != 0)
		{
			pthread_mutex_destroy(&sim->dongles[i].mutex);
			while (--i >= 0)
			{
				pthread_mutex_destroy(&sim->dongles[i].mutex);
				pthread_cond_destroy(&sim->dongles[i].cond);
				pq_free(sim->dongles[i].queue);
			}
			free(sim->coders);
			free(sim->threads);
			free(sim->dongles);
			pthread_mutex_destroy(&sim->print_mutex);
			pthread_mutex_destroy(&sim->state_mutex);
			return (1);
		}
		sim->dongles[i].available = 1;
		sim->dongles[i].last_release_ts = 0;
		sim->dongles[i].queue = pq_create(sim->scheduler[0] == 'e' ? 1 : 0);
		i++;
	}
	return (0);
}

/* Libertação de Recursos */
void sim_destroy_resources(t_sim *sim)
{
	int i;

	if (sim->dongles)
	{
		i = 0;
		while (i < sim->number_of_coders)
		{
			pthread_mutex_destroy(&sim->dongles[i].mutex);
			pthread_cond_destroy(&sim->dongles[i].cond);
			pq_free(sim->dongles[i].queue);
			i++;
		}
		free(sim->dongles);
	}
	pthread_mutex_destroy(&sim->print_mutex);
	pthread_mutex_destroy(&sim->state_mutex);
	free(sim->coders);
	free(sim->threads);
}

/* Gestão de Aquisição de Dongles com Segurança nas Filas e Cooldown */
int request_dongles(t_sim *sim, t_coder *coder)
{
	int first = coder->left;
	int second = coder->right;

	if (first == second)
	{
		pthread_mutex_lock(&sim->dongles[first].mutex);
		while (!get_sim_stop(sim))
			msleep(1);
		pthread_mutex_unlock(&sim->dongles[first].mutex);
		return (1);
	}

	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}

	t_pq_item item = {
		.id = coder->id,
		.arrival = timestamp_ms(),
		.deadline = get_coder_last_compile(sim, coder->id - 1) + sim->time_to_burnout
	};

	// Registo em ambas as filas mantendo a ordem estrita (first < second)
	pthread_mutex_lock(&sim->dongles[first].mutex);
	pq_push(sim->dongles[first].queue, item);
	pthread_mutex_unlock(&sim->dongles[first].mutex);

	pthread_mutex_lock(&sim->dongles[second].mutex);
	pq_push(sim->dongles[second].queue, item);
	pthread_mutex_unlock(&sim->dongles[second].mutex);

	// Ciclo de espera até conseguir ambos os dongles
	while (!get_sim_stop(sim))
	{
		pthread_mutex_lock(&sim->dongles[first].mutex);
		pthread_mutex_lock(&sim->dongles[second].mutex);

		t_pq_item top_first, top_second;
		int ok_first = (pq_peek(sim->dongles[first].queue, &top_first) == 0 && top_first.id == coder->id);
		int ok_second = (pq_peek(sim->dongles[second].queue, &top_second) == 0 && top_second.id == coder->id);

		if (ok_first && ok_second)
		{
			long long now = timestamp_ms();
			long long elapsed_first = now - sim->dongles[first].last_release_ts;
			long long elapsed_second = now - sim->dongles[second].last_release_ts;

			int cool_first = (sim->dongles[first].last_release_ts == 0 || elapsed_first >= sim->dongle_cooldown);
			int cool_second = (sim->dongles[second].last_release_ts == 0 || elapsed_second >= sim->dongle_cooldown);

			if (cool_first && cool_second)
			{
				t_pq_item dummy;
				pq_pop(sim->dongles[first].queue, &dummy);
				pq_pop(sim->dongles[second].queue, &dummy);
				
				// IMPORTANTE: Retornamos com os mutexes AINDA TRANCADOS.
				// Eles serão libertados mais tarde pela função release_dongles.
				return (0);
			}
		}

		pthread_mutex_unlock(&sim->dongles[second].mutex);
		pthread_mutex_unlock(&sim->dongles[first].mutex);

		msleep(1);
	}

	return (1);
}

void release_dongles(t_sim *sim, t_coder *coder)
{
	int first = coder->left;
	int second = coder->right;

	if (first == second)
	{
		pthread_mutex_unlock(&sim->dongles[first].mutex);
		return;
	}

	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}

	// Atualizar o timestamp de libertação e destrancar os mutexes na ordem correta
	sim->dongles[second].last_release_ts = timestamp_ms();
	pthread_mutex_unlock(&sim->dongles[second].mutex);

	sim->dongles[first].last_release_ts = timestamp_ms();
	pthread_mutex_unlock(&sim->dongles[first].mutex);
}

/* Getters e Setters Seguros com Mutex */

int get_sim_stop(t_sim *sim)
{
	int stop;

	pthread_mutex_lock(&sim->state_mutex);
	stop = sim->stop;
	pthread_mutex_unlock(&sim->state_mutex);
	return (stop);
}

void set_sim_stop(t_sim *sim, int val)
{
	pthread_mutex_lock(&sim->state_mutex);
	sim->stop = val;
	pthread_mutex_unlock(&sim->state_mutex);
}

long long get_coder_last_compile(t_sim *sim, int index)
{
	long long ts;

	pthread_mutex_lock(&sim->state_mutex);
	ts = sim->coders[index].last_compile_start;
	pthread_mutex_unlock(&sim->state_mutex);
	return (ts);
}

void set_coder_last_compile(t_sim *sim, int index, long long val)
{
	pthread_mutex_lock(&sim->state_mutex);
	sim->coders[index].last_compile_start = val;
	pthread_mutex_unlock(&sim->state_mutex);
}

int get_coder_compile_count(t_sim *sim, int index)
{
	int count;

	pthread_mutex_lock(&sim->state_mutex);
	count = sim->coders[index].compile_count;
	pthread_mutex_unlock(&sim->state_mutex);
	return (count);
}
