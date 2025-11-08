/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_base_fd.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 22:03:06 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/07 23:04:16 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

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

int	ft_putnbr_base_fd(long long nbr, char *base, int fd)
{
	unsigned long long	n;
	int	count;
	size_t	base_len;

	if (!confirm_base(base))
		return (0);
	count = 0;
	base_len = 0;
	while (base[base_len])
		base_len++;
	if (nbr < 0)
	{
		count += ft_putchar_fd('-', fd);
		n = (unsigned long long)(-nbr);
	}
	else
		n = (unsigned long long)nbr;
	if (n >= base_len)
		count += ft_putnbr_base_fd(n / base_len, base, fd);
	count += ft_putchar_fd(base[n % base_len], fd);
	return (count);
}