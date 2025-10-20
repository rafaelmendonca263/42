/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 20:40:01 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/16 20:27:26 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Puts all n caracters as NULL, start in s.
/// @param s(pointer)
/// @param n
void ft_bzero(void *s, size_t n)
{
    size_t	i;
	unsigned char *ptr;

	ptr = (unsigned char *)s;
	i = 0;
    while(i < n)
    {
        ptr[i] = '\0';
        i++;
    }
}
