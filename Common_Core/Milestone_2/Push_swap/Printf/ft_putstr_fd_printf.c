/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd_printf.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 13:09:33 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/14 13:12:54 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/// @brief Write a string in fd, without "\n".
/// @param s
/// @param fd
int	ft_putstr_fd_printf(char *s, int fd)
{
	int	i;

	i = 0;
	if (!s)
		return (write(fd, "(null)", 6), 6);
	while (s[i] != '\0')
	{
		ft_putchar_fd(s[i], fd);
		i++;
	}
	return (i);
}
