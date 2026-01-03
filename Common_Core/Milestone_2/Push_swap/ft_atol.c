/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atol.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/10 22:13:08 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 10:39:00 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Converts a str into a number: ex "-48" -> -48.
/// @param str
/// @return result

static void	ft_atol_checker(long *result, int sign, const char *nptr, int *i)
{
	if ((*result > 2147483647 && sign == 1) || (*result > 2147483648 && sign ==
			-1))
	{
		ft_printf("Error");
		exit(1);
	}
	*result = *result * 10 + (nptr[*i] - '0');
	(*i)++;
}

long	ft_atol(const char *nptr)
{
	int		i;
	int		sign;
	long	result;

	i = 0;
	sign = 1;
	result = 0;
	while ((nptr[i] >= 9 && nptr[i] <= 13) || nptr[i] == ' ')
		i++;
	if (nptr[i] == '+' || nptr[i] == '-')
	{
		if (nptr[i] == '-')
			sign = -1;
		i++;
	}
	if (nptr[i] < '0' || nptr[i] > '9')
		return (ft_printf("Error"), exit(1), 0);
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		ft_atol_checker(&result, sign, nptr, &i);
	}
	if (nptr[i] != '\0')
		return (ft_printf("Error"), exit(1), 0);
	return (result * sign);
}
