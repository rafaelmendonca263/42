/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim_utils.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:39:59 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 12:50:53 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

void	get_dongle_indices(t_coder *coder, int *f, int *s)
{
	*f = coder->left;
	*s = coder->right;
	if (*f > *s)
	{
		*f = coder->right;
		*s = coder->left;
	}
}

int	check_cooldown(t_sim *sim, int f, int s)
{
	long long	now;

	now = timestamp_ms();
	if (sim->dongles[f].last_release_ts
		&& now - sim->dongles[f].last_release_ts < sim->dongle_cooldown)
		return (1);
	if (sim->dongles[s].last_release_ts
		&& now - sim->dongles[s].last_release_ts < sim->dongle_cooldown)
		return (1);
	return (0);
}
