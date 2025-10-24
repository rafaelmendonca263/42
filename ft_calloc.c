/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 20:43:22 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 16:39:18 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief The calloc() function allocates memory for an array of  nmemb  elements
/// of  size bytes each and returns a pointer to the allocated memory.
/// @param nmemb
/// @param size
/// @return ptr
void	*ft_calloc(size_t nmemb, size_t size)
{
	int	*ptr;

	ptr = malloc(nmemb * size);
	if (!ptr)
		return (NULL);
	ft_bzero(ptr, nmemb * size);
	return (ptr);
}
