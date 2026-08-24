/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static int is_positive_number(const char *s)
{
	if (!s || !*s)
		return (0);
	for (size_t i = 0; s[i]; ++i)
		if (s[i] < '0' || s[i] > '9')
			return (0);
	return (1);
}

t_sim *init_sim(int argc, char **argv)
{
	(void)argc;
	t_sim *sim = malloc(sizeof(t_sim));
	if (!sim)
		return (NULL);
	if (!is_positive_number(argv[1]) || !is_positive_number(argv[2]) || !is_positive_number(argv[3]) || !is_positive_number(argv[4]) || !is_positive_number(argv[5]) || !is_positive_number(argv[6]) || !is_positive_number(argv[7]))
	{
		fprintf(stderr, "Invalid numeric arguments\n");
		free(sim);
		return (NULL);

	}
	sim->number_of_coders = atoi(argv[1]);
	sim->time_to_burnout = atoll(argv[2]);
	sim->time_to_compile = atoll(argv[3]);
	sim->time_to_debug = atoll(argv[4]);
	sim->time_to_refactor = atoll(argv[5]);
	sim->number_of_compiles_required = atoi(argv[6]);
	sim->dongle_cooldown = atoll(argv[7]);
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

void free_sim(t_sim *sim)
{
	free(sim);

}
