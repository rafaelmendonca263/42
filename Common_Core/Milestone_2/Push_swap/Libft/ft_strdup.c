/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 15:04:34 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/29 20:12:59 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief The  strdup() function returns a pointer
/// to a new string which is a duplicate of the string s.
/// Memory for the new string  is  obtained  with malloc(3),
/// and can be freed with free(3).
/// @param src
/// @return mem
char	*ft_strdup(const char *s)
{
	char	*mem;
	int		i;
	int		len;

	len = ft_strlen(s);
	mem = malloc(sizeof(char) * (len + 1));
	if (!mem)
		return (NULL);
	i = 0;
	while (i < len)
	{
		mem[i] = s[i];
		i++;
	}
	mem[i] = '\0';
	return (mem);
}
