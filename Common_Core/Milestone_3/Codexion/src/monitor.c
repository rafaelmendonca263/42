/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>

void *monitor_thread(void *arg)
{
	t_sim *sim = (t_sim *)arg;

	while (!sim->stop)
	{
		for (int i = 0; i < sim->number_of_coders; ++i)
		{
			t_coder *c = &sim->coders[i];
			long long now = timestamp_ms();
			long long deadline = c->last_compile_start + sim->time_to_burnout;

			if (now > deadline)
			{
				pthread_mutex_lock(&sim->print_mutex);
				print_log(sim, c->id, "burned out");
				pthread_mutex_unlock(&sim->print_mutex);
				sim->stop = 1;
				return (NULL);

			}
		}
		msleep(1);
	}
	return (NULL);
}
