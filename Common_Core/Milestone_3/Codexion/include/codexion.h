/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                 +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa            #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdint.h>
# include <sys/time.h>

typedef struct s_pq_item
{
	int id;
	long long deadline;
	long long arrival;
} t_pq_item;

typedef struct s_pq
{
	t_pq_item *items;
	int size;
	int capacity;
	int mode;
} t_pq;

typedef struct s_dongle
{
	pthread_mutex_t mutex;
	pthread_cond_t cond;
	int available;
	long long last_release_ts;
	t_pq *queue;
} t_dongle;

typedef struct s_coder
{
	int id;
	int left;
	int right;
	long long last_compile_start;
	int compile_count;
	struct s_sim *sim;
} t_coder;

typedef struct s_sim
{
	int number_of_coders;
	long long time_to_burnout;
	long long time_to_compile;
	long long time_to_debug;
	long long time_to_refactor;
	int number_of_compiles_required;
	long long dongle_cooldown;
	char scheduler[8];
	long long start_ts;
	pthread_mutex_t print_mutex;
	int stop;
	pthread_mutex_t state_mutex;
	int finished_count;
	t_dongle *dongles;
	t_coder *coders;
	pthread_t *threads;
	pthread_t monitor_thread;
} t_sim;

t_sim	*init_sim(int argc, char **argv);
void	free_sim(t_sim *sim);
long long	timestamp_ms(void);
void	msleep(long long ms);
void	print_log(t_sim *sim, int id, const char *msg);

t_pq	*pq_create(int mode);
void	pq_free(t_pq *pq);
int	pq_push(t_pq *pq, t_pq_item item);
int	pq_pop(t_pq *pq, t_pq_item *out);
int	pq_peek(t_pq *pq, t_pq_item *out);

int	sim_init_resources(t_sim *sim);
void	sim_destroy_resources(t_sim *sim);
int	request_dongles(t_sim *sim, t_coder *coder);
void	release_dongles(t_sim *sim, t_coder *coder);
void	*coder_thread(void *arg);
void	*monitor_thread(void *arg);

#endif
