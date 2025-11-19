/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 19:00:43 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/19 19:40:16 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/// @brief It works as a putchar but we can chose where we want to output.
/// @param c
/// @param fd
int	ft_putchar_fd(char c, int fd)
{
	write(fd, &c, 1);
	return (1);
}
