/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:48 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 12:43:29 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

long long	timestamp_ms(void)
{
	struct timespec	ts;

	clock_gettime(CLOCK_MONOTONIC, &ts);
	return ((long long)ts.tv_sec * 1000LL + (ts.tv_nsec / 1000000));
}

void	msleep(long long ms)
{
	long long	start;

	if (ms <= 0)
		return ;
	start = timestamp_ms();
	while ((timestamp_ms() - start) < ms)
		usleep(500);
}
