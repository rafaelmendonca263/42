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

char *ft_strtrim(char const *s1, char const *set)
{
    char *ptr;
    int i;
    int start;
    int end;

    if(!s1 || !set)
        return(NULL);
    i = 0;
    while(s1[i] && isset(s1[i], set))
        i++;
    start = i;
    i = ft_strlen(s1) - 1;
    while (s1[i] && isset(s1[i], set))
        i--;
    end = i;
    ptr = malloc(sizeof(char) * (end - start + 1));
    if (!ptr)
		return (NULL);
    i = 0;
    while(start <= end)
    {
        ptr[i] = s1[start];
        start++;
        i++;
    }
    ptr[i] = '\0';
    return(ptr);
}
int main()
{
    char *s1 = "/?GAYNILO//";
    char *set = "?//";
    printf("%s", ft_strtrim(s1,set));
    return(0);
}
