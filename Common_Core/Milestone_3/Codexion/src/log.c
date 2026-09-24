/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:25:32 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:25:34 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>

void	print_log(t_sim *sim, int id, const char *msg)
{
	long long	ts;

	ts = timestamp_ms() - sim->start_ts;
	printf("%lld %d %s\n", ts, id, msg);
}
