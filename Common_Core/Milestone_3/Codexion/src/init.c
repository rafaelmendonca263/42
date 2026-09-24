/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:42:46 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:46:44 by rmedonca         ###   ########.fr       */
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

static int	validate_args_basic(char **argv)
{
	if (!is_positive_number(argv[1]) || atoi(argv[1]) <= 0)
	{
		fprintf(stderr, "Error: invalid number_of_coders\n");
		return (0);
	}
	if (!is_positive_number(argv[2]) || atoi(argv[2]) <= 0)
	{
		fprintf(stderr, "Error: invalid time_to_burnout\n");
		return (0);
	}
	if (!is_positive_number(argv[3]) || atoi(argv[3]) <= 0)
	{
		fprintf(stderr, "Error: invalid time_to_compile\n");
		return (0);
	}
	if (!is_positive_number(argv[4]) || atoi(argv[4]) <= 0)
	{
		fprintf(stderr, "Error: invalid time_to_debug\n");
		return (0);
	}
	return (1);
}

static int	validate_args_extra(char **argv)
{
	if (!is_positive_number(argv[5]) || atoi(argv[5]) <= 0)
	{
		fprintf(stderr, "Error: invalid time_to_refactor\n");
		return (0);
	}
	if (!is_positive_number(argv[6]) || atoi(argv[6]) <= 0)
	{
		fprintf(stderr, "Error: invalid number_of_compiles\n");
		return (0);
	}
	if (!is_positive_number(argv[7]))
	{
		fprintf(stderr, "Error: invalid dongle_cooldown\n");
		return (0);
	}
	if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
	{
		fprintf(stderr, "Error: scheduler must be fifo/edf\n");
		return (0);
	}
	return (1);
}

static void	fill_sim(t_sim *sim, char **argv)
{
	sim->number_of_coders = atoi(argv[1]);
	sim->time_to_burnout = (long long)atoi(argv[2]);
	sim->time_to_compile = (long long)atoi(argv[3]);
	sim->time_to_debug = (long long)atoi(argv[4]);
	sim->time_to_refactor = (long long)atoi(argv[5]);
	sim->number_of_compiles_required = atoi(argv[6]);
	sim->dongle_cooldown = (long long)atoi(argv[7]);
}

t_sim	*init_sim(int argc, char **argv)
{
	t_sim	*sim;
	int		i;

	(void)argc;
	sim = malloc(sizeof(*sim));
	if (!sim)
		return (NULL);
	if (!validate_args_basic(argv) || !validate_args_extra(argv))
	{
		free(sim);
		return (NULL);
	}
	fill_sim(sim, argv);
	i = 0;
	while (argv[8][i] && i < (int) sizeof(sim ->scheduler) - 1)
	{
		sim->scheduler[i] = argv[8][i];
		i++;
	}
	sim->scheduler[i] = '\0';
	sim->start_ts = timestamp_ms();
	return (sim);
}
