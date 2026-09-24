/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim_init.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:24:15 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:36:42 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>

static int	sim_init_dongles(t_sim *sim, int i)
{
	int	mode;

	if (sim->scheduler[0] == 'e')
		mode = 1;
	else
		mode = 0;
	if (pthread_mutex_init(&sim->dongles[i].mutex, NULL) != 0)
		return (1);
	if (pthread_cond_init(&sim->dongles[i].cond, NULL) != 0)
	{
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		return (1);
	}
	sim->dongles[i].available = 1;
	sim->dongles[i].last_release_ts = 0;
	sim->dongles[i].queue = pq_create(mode);
	return (0);
}

static int	sim_alloc_resources(t_sim *sim)
{
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
	return (0);
}

int	sim_init_resources(t_sim *sim)
{
	int	i;

	sim->stop = 0;
	sim->finished_count = 0;
	if (sim_alloc_resources(sim) != 0)
		return (1);
	i = 0;
	while (i < sim->number_of_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].left = i;
		sim->coders[i].right = (i + 1) % sim->number_of_coders;
		sim->coders[i].last_compile_start = sim->start_ts;
		sim->coders[i].compile_count = 0;
		sim->coders[i].sim = sim;
		if (sim_init_dongles(sim, i) != 0)
			return (1);
		i++;
	}
	return (0);
}

void	sim_destroy_resources(t_sim *sim)
{
	int	i;

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

void	free_sim(t_sim *sim)
{
	if (!sim)
		return ;
	sim_destroy_resources(sim);
	free(sim);
}
