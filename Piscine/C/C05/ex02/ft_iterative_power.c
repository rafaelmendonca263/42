/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/11 18:28:22 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/17 17:20:00 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_iterative_power(int nb, int power)
{
	int	res;
	int	i;

	res = 1;
	if (power < 0)
		return (0);
	else if (power == 0)
		return (1);
	i = 0;
	while (i < power)
	{
		res = res * nb;
		i++;
	}
	return (res);
}
