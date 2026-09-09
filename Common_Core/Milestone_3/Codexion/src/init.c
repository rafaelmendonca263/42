/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                           :+:      :+:    :+:   */
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

static int	is_positive_number(const char *s)
{
	size_t	index;

	if (!s || !*s)
		return (0);
	index = 0;
	while (s[index])
	{
		if (s[index] < '0' || s[index] > '9')
			return (0);
		index++;
	}
	return (1);
}

static int	validate_args(char **argv)
{
	if (!is_positive_number(argv[1]))
		return (0);
	if (!is_positive_number(argv[2]))
		return (0);
	if (!is_positive_number(argv[3]))
		return (0);
	if (!is_positive_number(argv[4]))
		return (0);
	if (!is_positive_number(argv[5]))
		return (0);
	if (!is_positive_number(argv[6]))
		return (0);
	if (!is_positive_number(argv[7]))
		return (0);
	return (1);
}

static void	fill_sim(t_sim *sim, char **argv)
{
	sim->number_of_coders = atoi(argv[1]);
	sim->time_to_burnout = atoll(argv[2]);
	sim->time_to_compile = atoll(argv[3]);
	sim->time_to_debug = atoll(argv[4]);
	sim->time_to_refactor = atoll(argv[5]);
	sim->number_of_compiles_required = atoi(argv[6]);
	sim->dongle_cooldown = atoll(argv[7]);
}

t_sim	*init_sim(int argc, char **argv)
{
	t_sim	*sim;

	(void)argc;
	sim = malloc(sizeof(*sim));
	if (!sim)
		return (NULL);
	if (!validate_args(argv))
	{
		fprintf(stderr, "Invalid numeric arguments\n");
		free(sim);
		return (NULL);
	}
	fill_sim(sim, argv);
	if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
	{
		fprintf(stderr, "scheduler must be 'fifo' or 'edf'\n");
		free(sim);
		return (NULL);
	}
	strncpy(sim->scheduler, argv[8], sizeof(sim->scheduler) - 1);
	sim->scheduler[sizeof(sim->scheduler) - 1] = '\0';
	sim->start_ts = timestamp_ms();
	return (sim);
}

void	free_sim(t_sim *sim)
{
	free(sim);
}
