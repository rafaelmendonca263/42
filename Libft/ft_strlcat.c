/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 15:05:59 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 16:40:17 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Copy and concatenate strings respectively.
/// @param dest
/// @param src
/// @param size
/// @return

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	dst_len = 0;
	while (dst_len < size && dst[dst_len] != '\0')
		dst_len++;

	src_len = 0;
	while (src[src_len] != '\0')
		src_len++;

	i = 0;
	while ((dst_len + i + 1) < size && src[i] != '\0')
	{
		dst[dst_len + i] = src[i];
		i++;
	}

	if (dst_len + i < size)
		dst[dst_len + i] = '\0';

	return (dst_len + src_len);
}
