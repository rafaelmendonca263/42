/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:15 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 13:17:59 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	check_coder_compiles(t_sim *sim, t_coder *coder)
{
	int	res;

	pthread_mutex_lock(&sim->state_mutex);
	res = (coder->compile_count >= sim->number_of_compiles_required);
	pthread_mutex_unlock(&sim->state_mutex);
	return (res);
}

static void	coder_compile_action(t_sim *sim, t_coder *coder)
{
	int	should_stop;

	print_log(sim, coder->id, "has taken a dongle");
	print_log(sim, coder->id, "has taken a dongle");
	print_log(sim, coder->id, "is compiling");
	set_coder_last_compile(sim, coder->id - 1, timestamp_ms());
	msleep(sim->time_to_compile);
	should_stop = 0;
	pthread_mutex_lock(&sim->state_mutex);
	coder->compile_count++;
	if (coder->compile_count >= sim->number_of_compiles_required)
	{
		sim->finished_count++;
		if (sim->finished_count >= sim->number_of_coders)
			should_stop = 1;
	}
	pthread_mutex_unlock(&sim->state_mutex);
	if (should_stop)
		set_sim_stop(sim, 1);
	release_dongles(sim, coder);
}

static int	coder_debug_refactor(t_sim *sim, t_coder *coder)
{
	if (get_sim_stop(sim) || check_coder_compiles(sim, coder))
		return (1);
	print_log(sim, coder->id, "is debugging");
	msleep(sim->time_to_debug);
	if (get_sim_stop(sim) || check_coder_compiles(sim, coder))
		return (1);
	print_log(sim, coder->id, "is refactoring");
	msleep(sim->time_to_refactor);
	return (0);
}

void	*coder_thread(void *arg)
{
	t_coder	*coder;
	t_sim	*sim;

	coder = (t_coder *)arg;
	sim = coder->sim;
	while (!get_sim_stop(sim))
	{
		if (check_coder_compiles(sim, coder))
			break ;
		if (request_dongles(sim, coder) != 0)
			break ;
		if (get_sim_stop(sim))
		{
			release_dongles(sim, coder);
			break ;
		}
		coder_compile_action(sim, coder);
		if (coder_debug_refactor(sim, coder))
			break ;
	}
	return (NULL);
}
