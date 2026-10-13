/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim_init.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:41 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 18:47:37 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

void	sim_destroy_resources(t_sim *sim)
{
	int	i;

	if (!sim)
		return ;
	if (sim->dongles)
	{
		i = -1;
		while (++i < sim->number_of_coders)
		{
			pthread_mutex_destroy(&sim->dongles[i].mutex);
			if (sim->dongles[i].queue)
				pq_free(sim->dongles[i].queue);
		}
		free(sim->dongles);
		sim->dongles = NULL;
	}
	pthread_mutex_destroy(&sim->print_mutex);
	pthread_mutex_destroy(&sim->state_mutex);
	if (sim->coders)
		free(sim->coders);
	if (sim->threads)
		free(sim->threads);
}

void	free_sim(t_sim *sim)
{
	if (!sim)
		return ;
	sim_destroy_resources(sim);
	free(sim);
}

static int	sim_init_dongles(t_sim *sim)
{
	int	i;
	int	mode;

	mode = (strcmp(sim->scheduler, "edf") == 0);
	sim->dongles = malloc(sizeof(t_dongle) * sim->number_of_coders);
	if (!sim->dongles)
		return (0);
	i = 0;
	while (i < sim->number_of_coders)
	{
		if (pthread_mutex_init(&sim->dongles[i].mutex, NULL) != 0)
			return (0);
		sim->dongles[i].available = 1;
		sim->dongles[i].last_release_ts = 0;
		sim->dongles[i].queue = pq_create(mode);
		if (!sim->dongles[i].queue)
			return (0);
		i++;
	}
	return (1);
}

static void	sim_init_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->number_of_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].left = i;
		sim->coders[i].right = (i + 1) % sim->number_of_coders;
		sim->coders[i].last_compile_start = sim->start_ts;
		sim->coders[i].compile_count = 0;
		sim->coders[i].sim = sim;
		i++;
	}
}

int	sim_init_resources(t_sim *sim)
{
	if (pthread_mutex_init(&sim->print_mutex, NULL) != 0)
		return (0);
	if (pthread_mutex_init(&sim->state_mutex, NULL) != 0)
		return (0);
	sim->coders = malloc(sizeof(t_coder) * sim->number_of_coders);
	sim->threads = malloc(sizeof(pthread_t) * sim->number_of_coders);
	if (!sim->coders || !sim->threads)
	{
		sim_destroy_resources(sim);
		return (0);
	}
	if (!sim_init_dongles(sim))
	{
		sim_destroy_resources(sim);
		return (0);
	}
	sim_init_coders(sim);
	return (1);
}
