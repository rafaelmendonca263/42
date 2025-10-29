/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 20:40:40 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/29 19:29:03 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Do a print bit by bit from src to dest with
/// size n. It solved if the memory areas do overlap.
/// @param dest
/// @param src
/// @param n
/// @return dest
void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char		*d;
	const unsigned char	*s = src;
	size_t				i;

	d = dest;
	if (!dest && !src)
		return (NULL);
	if (d < s)
	{
		i = 0;
		while (i < n)
		{
			d[i] = s[i];
			i++;
		}
		return (dest);
	}
	i = n;
	while (i > 0)
	{
		i--;
		d[i] = s[i];
	}
	return (dest);
}
