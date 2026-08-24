/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>

void print_log(t_sim *sim, int id, const char *msg)
{
	long long ts = timestamp_ms() - sim->start_ts;
	char buf[128];
	int len = snprintf(buf, sizeof(buf), "%lld %d %s\n", ts, id, msg);

	if (len > 0)
		write(STDOUT_FILENO, buf, (size_t)len);
}
