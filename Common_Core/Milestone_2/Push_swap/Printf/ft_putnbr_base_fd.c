/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_base_fd.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 14:11:01 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/14 14:11:03 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	confirm_base(char *base)
{
	int	i;
	int	j;

	i = 0;
	while (base[i])
	{
		if (base[i] == '+' || base[i] == '-')
			return (0);
		j = i + 1;
		while (base[j])
		{
			if (base[i] == base[j])
				return (0);
			j++;
		}
		i++;
	}
	return (i >= 2);
}

int	ft_putnbr_base_fd(unsigned long long nbr, char *base, int fd)
{
	size_t	base_len;
	int		count;

	if (!confirm_base(base))
		return (0);
	count = 0;
	base_len = 0;
	while (base[base_len])
		base_len++;
	if (nbr >= base_len)
		count += ft_putnbr_base_fd(nbr / base_len, base, fd);
	count += ft_putchar_fd((base[nbr % base_len]), fd);
	return (count);
}
