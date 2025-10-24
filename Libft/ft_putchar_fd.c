/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 19:00:43 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 16:39:52 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief It works as a putchar but we can chose where we want to output.
/// @param c
/// @param fd
void	ft_putchar_fd(char c, int fd)
{
	write(fd, &c, 1);
}
