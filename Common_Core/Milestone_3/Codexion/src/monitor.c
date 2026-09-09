/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                 +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa            #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>

void	*monitor_thread(void *arg)
{
	t_sim	*sim;
	int		index;
	long long	now;
	long long	deadline;

	sim = (t_sim *)arg;
	while (!sim->stop)
	{
		index = 0;
		while (index < sim->number_of_coders)
		{
			now = timestamp_ms();
			deadline = sim->coders[index].last_compile_start
				+ sim->time_to_burnout;
			if (now > deadline)
			{
				pthread_mutex_lock(&sim->print_mutex);
				print_log(sim, sim->coders[index].id, "burned out");
				pthread_mutex_unlock(&sim->print_mutex);
				sim->stop = 1;
				return (NULL);
			}
			index++;
		}
		msleep(1);
	}
	return (NULL);
}
