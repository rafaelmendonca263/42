/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   getters.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:23:31 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:43:54 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

int	get_sim_stop(t_sim *sim)
{
	int	res;

	pthread_mutex_lock(&sim->state_mutex);
	res = sim->stop;
	pthread_mutex_unlock(&sim->state_mutex);
	return (res);
}

void	set_sim_stop(t_sim *sim, int val)
{
	pthread_mutex_lock(&sim->state_mutex);
	sim->stop = val;
	pthread_mutex_unlock(&sim->state_mutex);
}

long long	get_coder_last_compile(t_sim *sim, int idx)
{
	long long	ts;

	pthread_mutex_lock(&sim->state_mutex);
	ts = sim->coders[idx].last_compile_start;
	pthread_mutex_unlock(&sim->state_mutex);
	return (ts);
}

void	set_coder_last_compile(t_sim *sim, int idx, long long ts)
{
	pthread_mutex_lock(&sim->state_mutex);
	sim->coders[idx].last_compile_start = ts;
	pthread_mutex_unlock(&sim->state_mutex);
}
