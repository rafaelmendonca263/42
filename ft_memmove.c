/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 20:40:40 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 16:39:46 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Do a print bit by bit from src to dest with size n. It solved if the memory areas do overlap.
/// @param dest
/// @param src
/// @param n
/// @return dest
void	*ft_memmove(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*ptr_dest;
	const unsigned char	*ptr_src;

	ptr_dest = (unsigned char *)dest;
	ptr_src = (const unsigned char *)src;
	i = 0;
	if (ptr_dest < ptr_src)
	{
        while(i < n)
		{
            ptr_dest[i] = ptr_src[i];
		    i++;
        }
	}
	else if(ptr_dest > ptr_src)
	{
        i = n;
        while(i > 0)
        {
            i--;
		    ptr_dest[i] = ptr_src[i];
        }
    }
	return (dest);
}
