/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int sim_init_resources(t_sim *sim)
{
	int i;
	sim->dongles = malloc(sizeof(t_dongle) * sim->number_of_coders);
	if (!sim->dongles) return -1;
	sim->coders = malloc(sizeof(t_coder) * sim->number_of_coders);
	if (!sim->coders) { free(sim->dongles);

 return -1;
 }
	sim->threads = malloc(sizeof(pthread_t) * sim->number_of_coders);
	if (!sim->threads) { free(sim->dongles);
 free(sim->coders);
 return -1;
 }
	pthread_mutex_init(&sim->print_mutex, NULL);
 pthread_mutex_init(&sim->state_mutex, NULL);
	sim->stop = 0;
 sim->finished_count = 0;
	for (i = 0; i < sim->number_of_coders; ++i) {
		pthread_mutex_init(&sim->dongles[i].mutex, NULL);

 pthread_cond_init(&sim->dongles[i].cond, NULL);
		sim->dongles[i].available = 1;
 sim->dongles[i].last_release_ts = sim->start_ts;
		sim->dongles[i].queue = pq_create(strcmp(sim->scheduler, "fifo") == 0 ? 0 : 1);
		sim->coders[i].id = i + 1;
 sim->coders[i].left = i;
 sim->coders[i].right = (i + 1) % sim->number_of_coders;
		sim->coders[i].last_compile_start = sim->start_ts;
 sim->coders[i].compile_count = 0;
 sim->coders[i].sim = sim;
	}
	return (0);
}

void sim_destroy_resources(t_sim *sim)
{
	int i;
	if (!sim) return;

	for (i = 0; i < sim->number_of_coders; ++i)
	{
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		pthread_cond_destroy(&sim->dongles[i].cond);
		pq_free(sim->dongles[i].queue);

	}
	pthread_mutex_destroy(&sim->print_mutex);
	pthread_mutex_destroy(&sim->state_mutex);
	free(sim->dongles);
	free(sim->coders);
	free(sim->threads);
}

int request_dongles(t_sim *sim, t_coder *coder)
{
	int l = coder->left, r = coder->right;

 long long now = timestamp_ms();
 t_pq_item item;
	item.id = coder->id;
 item.arrival = now;
 item.deadline = coder->last_compile_start + sim->time_to_burnout;
	if (l == r) { pthread_mutex_lock(&sim->dongles[l].mutex);
 pq_push(sim->dongles[l].queue, item);
 pthread_mutex_unlock(&sim->dongles[l].mutex);
 while (!sim->stop) msleep(1);
 return -1;
 }
	pthread_mutex_lock(&sim->dongles[l].mutex);
 pq_push(sim->dongles[l].queue, item);
 pthread_mutex_unlock(&sim->dongles[l].mutex);
	pthread_mutex_lock(&sim->dongles[r].mutex);
 pq_push(sim->dongles[r].queue, item);
 pthread_mutex_unlock(&sim->dongles[r].mutex);
	while (!sim->stop)
	{
		int first = l < r ? l : r, second = l < r ? r : l;
		pthread_mutex_lock(&sim->dongles[first].mutex);

 pthread_mutex_lock(&sim->dongles[second].mutex);
		t_pq_item peek1, peek2;
 int ok1 = (pq_peek(sim->dongles[l].queue, &peek1) == 0 && peek1.id == coder->id);
		int ok2 = (pq_peek(sim->dongles[r].queue, &peek2) == 0 && peek2.id == coder->id);
		long long now2 = timestamp_ms();
		int avail1 = sim->dongles[l].available && (now2 - sim->dongles[l].last_release_ts >= sim->dongle_cooldown);
		int avail2 = sim->dongles[r].available && (now2 - sim->dongles[r].last_release_ts >= sim->dongle_cooldown);
		if (ok1 && ok2 && avail1 && avail2) { pq_pop(sim->dongles[l].queue, NULL);
 pq_pop(sim->dongles[r].queue, NULL);
 sim->dongles[l].available = 0;
 sim->dongles[r].available = 0;
 pthread_mutex_unlock(&sim->dongles[second].mutex);
 pthread_mutex_unlock(&sim->dongles[first].mutex);
 return 0;
 }
		pthread_mutex_unlock(&sim->dongles[second].mutex);
 pthread_mutex_unlock(&sim->dongles[first].mutex);
 msleep(1);
	}
	return (-1);
}

void release_dongles(t_sim *sim, t_coder *coder)
{
	int l = coder->left;
	int r = coder->right;
	long long now = timestamp_ms();
	pthread_mutex_lock(&sim->dongles[l].mutex);
	sim->dongles[l].available = 1;
	sim->dongles[l].last_release_ts = now;
	pthread_cond_broadcast(&sim->dongles[l].cond);
	pthread_mutex_unlock(&sim->dongles[l].mutex);
	pthread_mutex_lock(&sim->dongles[r].mutex);
	sim->dongles[r].available = 1;
	sim->dongles[r].last_release_ts = now;
	pthread_cond_broadcast(&sim->dongles[r].cond);
	pthread_mutex_unlock(&sim->dongles[r].mutex);

}
