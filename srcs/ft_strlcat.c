/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/10 20:21:30 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/16 18:47:45 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

unsigned int	ft_strlcat(char *dest, char *src, unsigned int size)
{
	unsigned int	dest_len;
	unsigned int	src_len;
	unsigned int	i;

	if (!dest || !src)
		return (0);
	dest_len = 0;
	while (dest_len < size && dest[dest_len] != '\0')
		dest_len++;
	src_len = ft_strlen(src);
	if (dest_len == size)
		return (size + src_len);
	i = 0;
	while ((dest_len + i + 1) < size && src[i] != '\0')
	{
		dest[dest_len + i] = src[i];
		i++;
	}
	if (dest_len + i < size)
		dest[dest_len + i] = '\0';
	else if (size > 0)
		dest[size - 1] = '\0';
	return (dest_len + src_len);
}
