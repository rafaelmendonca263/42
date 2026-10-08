/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:44 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 12:50:49 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	check_dongles_ready(t_sim *sim, t_coder *coder, int f, int s)
{
	t_pq_item	tf;
	t_pq_item	ts;

	if (!sim->dongles[f].available || !sim->dongles[s].available)
		return (0);
	if (pq_peek(sim->dongles[f].queue, &tf) || tf.id != coder->id
		|| pq_peek(sim->dongles[s].queue, &ts) || ts.id != coder->id)
		return (0);
	if (check_cooldown(sim, f, s))
		return (0);
	pq_pop(sim->dongles[f].queue, &tf);
	pq_pop(sim->dongles[s].queue, &ts);
	sim->dongles[f].available = 0;
	sim->dongles[s].available = 0;
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
	int	got;

	if (coder->left == coder->right)
		return (request_single_dongle(sim, coder->left));
	get_dongle_indices(coder, &f, &s);
	push_dongles(sim, coder, f, s);
	while (!get_sim_stop(sim))
	{
		pthread_mutex_lock(&sim->dongles[f].mutex);
		pthread_mutex_lock(&sim->dongles[s].mutex);
		got = check_dongles_ready(sim, coder, f, s);
		pthread_mutex_unlock(&sim->dongles[s].mutex);
		pthread_mutex_unlock(&sim->dongles[f].mutex);
		if (got)
			return (0);
		msleep(1);
	}
	return (1);
}

void	release_dongles(t_sim *sim, t_coder *coder)
{
	int	f;
	int	s;

	if (coder->left == coder->right)
		return ;
	get_dongle_indices(coder, &f, &s);
	pthread_mutex_lock(&sim->dongles[f].mutex);
	pthread_mutex_lock(&sim->dongles[s].mutex);
	sim->dongles[f].available = 1;
	sim->dongles[f].last_release_ts = timestamp_ms();
	sim->dongles[s].available = 1;
	sim->dongles[s].last_release_ts = timestamp_ms();
	pthread_mutex_unlock(&sim->dongles[s].mutex);
	pthread_mutex_unlock(&sim->dongles[f].mutex);
}
