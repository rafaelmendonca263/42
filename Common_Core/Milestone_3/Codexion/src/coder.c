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

	while (!get_sim_stop(sim))
	{
		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
			break;
		if (request_dongles(sim, coder) != 0)
			break;
		

		if (get_sim_stop(sim))
		{
			release_dongles(sim, coder);
			break;
		}

		/* taken two dongles */
		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "has taken a dongle");
		print_log(sim, coder->id, "has taken a dongle");
		print_log(sim, coder->id, "is compiling");
		pthread_mutex_unlock(&sim->print_mutex);
		
		set_coder_last_compile(sim, coder->id - 1, timestamp_ms());
		msleep(sim->time_to_compile);

		if (get_sim_stop(sim))
		{
			release_dongles(sim, coder);
			break;
		}
			
		pthread_mutex_lock(&sim->state_mutex);
		coder->compile_count++;
		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
		{
			sim->finished_count++;
			if (sim->finished_count >= sim->number_of_coders)
				sim->stop = 1;
		}
		pthread_mutex_unlock(&sim->state_mutex);
		
		release_dongles(sim, coder);
		if (get_sim_stop(sim))
			break;

		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "is debugging");
		pthread_mutex_unlock(&sim->print_mutex);
		
		msleep(sim->time_to_debug);
		if (get_sim_stop(sim))
			break;

		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, coder->id, "is refactoring");
		pthread_mutex_unlock(&sim->print_mutex);
		
		msleep(sim->time_to_refactor);
		if (get_sim_stop(sim))
			break;

		if (sim->number_of_compiles_required > 0 && coder->compile_count >= sim->number_of_compiles_required)
			break;
	}
	return (NULL);
}
