/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 18:59:38 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 20:13:32 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int isset(char c, char const *set)
{
    int i;

    i = 0;
    while(set[i])
    {
        if(set[i] == c)
            return(1);
        i++;
    }
    return(0);
}

static int get_trim_indices(const char *s1, const char *set, int *start, int *end)
{
    *start = 0;
    while (s1[*start] && isset(s1[*start], set))
        (*start)++;
    *end = ft_strlen(s1) - 1;
    while (*end >= *start && isset(s1[*end], set))
        (*end)--;
    return (*end < *start);
}

char *ft_strtrim(char const *s1, char const *set)
{
    char *ptr;
    int start, end, i;
    if (!s1 || !set)
        return NULL;
    if (get_trim_indices(s1, set, &start, &end))
    {
        ptr = malloc(1);
        if (!ptr) return NULL;
        ptr[0] = '\0';
        return ptr;
    }
    ptr = malloc(sizeof(char) * (end - start + 2));
    if (!ptr)
        return NULL;
    i = 0;
    while (start <= end)
        ptr[i++] = s1[start++];
    ptr[i] = '\0';
    return ptr;
}
