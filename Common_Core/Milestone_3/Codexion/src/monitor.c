/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:25:10 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 19:48:02 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	check_coder_burnout(t_sim *sim, int index)
{
	long long	now;
	long long	deadline;

	now = timestamp_ms();
	deadline = get_coder_last_compile(sim, index)
		+ sim->time_to_burnout;
	if (now > deadline)
	{
		pthread_mutex_lock(&sim->print_mutex);
		print_log(sim, sim->coders[index].id, "burned out");
		pthread_mutex_unlock(&sim->print_mutex);
		set_sim_stop(sim, 1);
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
