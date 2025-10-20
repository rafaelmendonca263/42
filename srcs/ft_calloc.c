/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 20:43:22 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/20 19:19:13 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief 
/// @param nmemb 
/// @param size 
/// @return 
void *calloc(size_t nmemb, size_t size)
{
    void *ptr;
 
    ptr = calloc(nmemb, size);
    if (!ptr)
    {
        
    }
    free(ptr)
}
