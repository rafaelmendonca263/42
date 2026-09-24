/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:24:48 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:43:38 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	check_dongles_ready(t_sim *sim, t_coder *coder, int f, int s)
{
	t_pq_item	tf;
	t_pq_item	ts;
	long long	now;

	if (pq_peek(sim->dongles[f].queue, &tf) != 0 || tf.id != coder->id)
		return (0);
	if (pq_peek(sim->dongles[s].queue, &ts) != 0 || ts.id != coder->id)
		return (0);
	now = timestamp_ms();
	if (sim->dongles[f].last_release_ts != 0
		&& now - sim->dongles[f].last_release_ts < sim->dongle_cooldown)
		return (0);
	if (sim->dongles[s].last_release_ts != 0
		&& now - sim->dongles[s].last_release_ts < sim->dongle_cooldown)
		return (0);
	pq_pop(sim->dongles[f].queue, &tf);
	pq_pop(sim->dongles[s].queue, &ts);
	return (1);
}

static void	push_dongles(t_sim *sim, t_coder *coder, int f, int s)
{
	t_pq_item	item;

	item.id = coder->id;
	item.arrival = timestamp_ms();
	item.deadline = get_coder_last_compile(sim, coder->id - 1)
		+ sim->time_to_burnout;
	pthread_mutex_lock(&sim->dongles[f].mutex);
	pq_push(sim->dongles[f].queue, item);
	pthread_mutex_unlock(&sim->dongles[f].mutex);
	pthread_mutex_lock(&sim->dongles[s].mutex);
	pq_push(sim->dongles[s].queue, item);
	pthread_mutex_unlock(&sim->dongles[s].mutex);
}

static int	request_single_dongle(t_sim *sim, int f)
{
	pthread_mutex_lock(&sim->dongles[f].mutex);
	while (!get_sim_stop(sim))
		msleep(1);
	pthread_mutex_unlock(&sim->dongles[f].mutex);
	return (1);
}

int	request_dongles(t_sim *sim, t_coder *coder)
{
	int	f;
	int	s;

	f = coder->left;
	s = coder->right;
	if (f == s)
		return (request_single_dongle(sim, f));
	if (f > s)
	{
		f = coder->right;
		s = coder->left;
	}
	push_dongles(sim, coder, f, s);
	while (!get_sim_stop(sim))
	{
		pthread_mutex_lock(&sim->dongles[f].mutex);
		pthread_mutex_lock(&sim->dongles[s].mutex);
		if (check_dongles_ready(sim, coder, f, s))
			return (0);
		pthread_mutex_unlock(&sim->dongles[s].mutex);
		pthread_mutex_unlock(&sim->dongles[f].mutex);
		msleep(1);
	}
	return (1);
}

void	release_dongles(t_sim *sim, t_coder *coder)
{
	int	f;
	int	s;

	f = coder->left;
	s = coder->right;
	if (f == s)
	{
		pthread_mutex_unlock(&sim->dongles[f].mutex);
		return ;
	}
	if (f > s)
	{
		f = coder->right;
		s = coder->left;
	}
	sim->dongles[s].last_release_ts = timestamp_ms();
	pthread_mutex_unlock(&sim->dongles[s].mutex);
	sim->dongles[f].last_release_ts = timestamp_ms();
	pthread_mutex_unlock(&sim->dongles[f].mutex);
}
