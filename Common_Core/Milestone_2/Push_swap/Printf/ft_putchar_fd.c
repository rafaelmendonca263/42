/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 19:00:43 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/14 13:13:03 by rmedonca         ###   ########.fr       */
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
