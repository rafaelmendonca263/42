/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 19:00:43 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/07 22:01:01 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief It works as a putchar but we can chose where we want to output.
/// @param c
/// @param fd
int	ft_putchar_fd(char c, int fd)
{
	write(fd, &c, 1);
	return (1);
}
