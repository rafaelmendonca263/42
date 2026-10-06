/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:25:32 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/06 16:23:17 by rafa             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

void	print_log(t_sim *sim, int id, const char *msg)
{
	long long	ts;

	pthread_mutex_lock(&sim->print_mutex);
	if (!get_sim_stop(sim) || strcmp(msg, "burned out") == 0)
	{
		ts = timestamp_ms() - sim->start_ts;
		printf("%lld %d %s\n", ts, id, msg);
	}
	pthread_mutex_unlock(&sim->print_mutex);
}
