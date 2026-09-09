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
#include <string.h>

int	sim_init_resources(t_sim *sim)
{
	int		index;
	int		ok;

	if (!sim)
		return (-1);
	sim->dongles = malloc(sizeof(t_dongle) * sim->number_of_coders);
	sim->coders = malloc(sizeof(t_coder) * sim->number_of_coders);
	sim->threads = malloc(sizeof(pthread_t) * sim->number_of_coders);
	if (!sim->dongles || !sim->coders || !sim->threads)
	{
		free(sim->dongles);
		free(sim->coders);
		free(sim->threads);
		return (-1);
	}
	ok = pthread_mutex_init(&sim->print_mutex, NULL);
	if (ok != 0)
		return (-1);
	ok = pthread_mutex_init(&sim->state_mutex, NULL);
	if (ok != 0)
		return (-1);
	sim->stop = 0;
	sim->finished_count = 0;
	index = 0;
	while (index < sim->number_of_coders)
	{
		ok = pthread_mutex_init(&sim->dongles[index].mutex, NULL);
		if (ok != 0)
			return (-1);
		ok = pthread_cond_init(&sim->dongles[index].cond, NULL);
		if (ok != 0)
			return (-1);
		sim->dongles[index].available = 1;
		sim->dongles[index].last_release_ts = sim->start_ts;
		if (strcmp(sim->scheduler, "fifo") == 0)
			sim->dongles[index].queue = pq_create(0);
		else
			sim->dongles[index].queue = pq_create(1);
		if (!sim->dongles[index].queue)
			return (-1);
		sim->coders[index].id = index + 1;
		sim->coders[index].left = index;
		sim->coders[index].right = (index + 1) % sim->number_of_coders;
		sim->coders[index].last_compile_start = sim->start_ts;
		sim->coders[index].compile_count = 0;
		sim->coders[index].sim = sim;
		index++;
	}
	return (0);
}

void	sim_destroy_resources(t_sim *sim)
{
	int		index;

	if (!sim)
		return ;
	index = 0;
	while (index < sim->number_of_coders)
	{
		pthread_mutex_destroy(&sim->dongles[index].mutex);
		pthread_cond_destroy(&sim->dongles[index].cond);
		pq_free(sim->dongles[index].queue);
		index++;
	}
	pthread_mutex_destroy(&sim->print_mutex);
	pthread_mutex_destroy(&sim->state_mutex);
	free(sim->dongles);
	free(sim->coders);
	free(sim->threads);
}

int	request_dongles(t_sim *sim, t_coder *coder)
{
	int		left;
	int		right;
	t_pq_item	item;
	long long	now;
	t_pq_item	peek_left;
	t_pq_item	peek_right;
	int		ready_left;
	int		ready_right;

	left = coder->left;
	right = coder->right;
	now = timestamp_ms();
	item.id = coder->id;
	item.arrival = now;
	item.deadline = coder->last_compile_start + sim->time_to_burnout;
	pthread_mutex_lock(&sim->dongles[left].mutex);
	pq_push(sim->dongles[left].queue, item);
	pthread_mutex_unlock(&sim->dongles[left].mutex);
	pthread_mutex_lock(&sim->dongles[right].mutex);
	pq_push(sim->dongles[right].queue, item);
	pthread_mutex_unlock(&sim->dongles[right].mutex);
	while (!sim->stop)
	{
		ready_left = pq_peek(sim->dongles[left].queue, &peek_left) == 0
			&& peek_left.id == coder->id;
		ready_right = pq_peek(sim->dongles[right].queue, &peek_right) == 0
			&& peek_right.id == coder->id;
		if (ready_left && ready_right && sim->dongles[left].available
			&& sim->dongles[right].available && now - sim->dongles[left].last_release_ts
			>= sim->dongle_cooldown && now - sim->dongles[right].last_release_ts
			>= sim->dongle_cooldown)
		{
			pq_pop(sim->dongles[left].queue, NULL);
			pq_pop(sim->dongles[right].queue, NULL);
			sim->dongles[left].available = 0;
			sim->dongles[right].available = 0;
			return (0);
		}
		msleep(1);
		now = timestamp_ms();
	}
	return (-1);
}

void	release_dongles(t_sim *sim, t_coder *coder)
{
	int		left;
	int		right;
	long long	now;

	left = coder->left;
	right = coder->right;
	now = timestamp_ms();
	pthread_mutex_lock(&sim->dongles[left].mutex);
	sim->dongles[left].available = 1;
	sim->dongles[left].last_release_ts = now;
	pthread_cond_broadcast(&sim->dongles[left].cond);
	pthread_mutex_unlock(&sim->dongles[left].mutex);
	pthread_mutex_lock(&sim->dongles[right].mutex);
	sim->dongles[right].available = 1;
	sim->dongles[right].last_release_ts = now;
	pthread_cond_broadcast(&sim->dongles[right].cond);
	pthread_mutex_unlock(&sim->dongles[right].mutex);
}
