/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                           :+:      :+:    :+:   */
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

static void	start_threads(t_sim *sim)
{
	int		i;

	i = 0;
	while (i < sim->number_of_coders)
	{
		pthread_create(&sim->threads[i], NULL, coder_thread, &sim->coders[i]);
		i++;
	}
	pthread_create(&sim->monitor_thread, NULL, monitor_thread, sim);
}

static void	join_threads(t_sim *sim)
{
	int		i;

	i = 0;
	while (i < sim->number_of_coders)
	{
		pthread_join(sim->threads[i], NULL);
		i++;
	}
	sim->stop = 1;
	pthread_join(sim->monitor_thread, NULL);
}

int	main(int argc, char **argv)
{
	t_sim	*sim;

	if (argc != 9)
	{
		fprintf(stderr,
			"Usage: %s number_of_coders time_to_burnout "
			"time_to_compile time_to_debug time_to_refactor "
			"number_of_compiles_required dongle_cooldown scheduler\n",
			argv[0]);
		return (1);
	}
	sim = init_sim(argc, argv);
	if (!sim)
		return (1);
	if (sim_init_resources(sim) != 0)
	{
		fprintf(stderr, "Failed to init resources\n");
		free_sim(sim);
		return (1);
	}
	start_threads(sim);
	join_threads(sim);
	sim_destroy_resources(sim);
	free_sim(sim);
	return (0);
}
