/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:33 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 12:25:23 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	is_coder_finished(t_sim *sim, int index)
{
	int	finished;

	finished = 0;
	pthread_mutex_lock(&sim->state_mutex);
	if (sim->number_of_compiles_required > 0
		&& sim->coders[index].compile_count >= sim->number_of_compiles_required)
		finished = 1;
	pthread_mutex_unlock(&sim->state_mutex);
	return (finished);
}

static int	check_coder_burnout(t_sim *sim, int index)
{
	long long	now;
	long long	deadline;

	if (is_coder_finished(sim, index))
		return (0);
	now = timestamp_ms();
	deadline = get_coder_last_compile(sim, index)
		+ sim->time_to_burnout;
	if (now > deadline)
	{
		set_sim_stop(sim, 1);
		print_log(sim, sim->coders[index].id, "burned out");
		return (1);
	}
	return (0);
}

void	*monitor_thread(void *arg)
{
	t_sim	*sim;
	int		index;

	sim = (t_sim *)arg;
	while (!get_sim_stop(sim))
	{
		index = 0;
		while (index < sim->number_of_coders)
		{
			if (check_coder_burnout(sim, index))
				return (NULL);
			index++;
		}
		usleep(200);
	}
	return (NULL);
}
