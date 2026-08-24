/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>

void *coder_thread(void *arg)
{
	t_coder *coder = (t_coder *)arg;
	t_sim *sim = coder->sim;

	while (!sim->stop)
	{
		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
			break;
		if (request_dongles(sim, coder) != 0)
			break;
		/* taken two dongles */
		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "has taken a dongle");
		print_log(sim, coder->id, "has taken a dongle");
		print_log(sim, coder->id, "is compiling");
		pthread_mutex_unlock(&sim->print_mutex);
		coder->last_compile_start = timestamp_ms();
		msleep(sim->time_to_compile);
		coder->compile_count++;
		/* If reached required compile count, update finished counter and stop if all done (do it immediately after compiling) */
		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
		{
			pthread_mutex_lock(&sim->state_mutex);
			sim->finished_count++;

			if (sim->finished_count >= sim->number_of_coders)
				sim->stop = 1;
			pthread_mutex_unlock(&sim->state_mutex);
		}
		release_dongles(sim, coder);
		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "is debugging");
		pthread_mutex_unlock(&sim->print_mutex);
		msleep(sim->time_to_debug);
		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "is refactoring");
		pthread_mutex_unlock(&sim->print_mutex);
		msleep(sim->time_to_refactor);
		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
			break;
	}
	return (NULL);
}
