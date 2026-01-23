/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 19:01:32 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/14 14:44:43 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/// @brief Write a number in fd.
/// @param n
/// @param fd
void	ft_putnbr_fd(int n, int fd)
{
	if (n == -2147483648)
	{
		ft_putstr_fd_printf("-2147483648", fd);
		return ;
	}
	if (n < 0)
	{
		ft_putchar_fd('-', fd);
		n = n * -1;
	}
	if (n <= 9)
	{
		ft_putchar_fd((n + '0'), fd);
		return ;
	}
	ft_putnbr_fd((n / 10), fd);
	ft_putchar_fd((n % 10) + '0', fd);
}
