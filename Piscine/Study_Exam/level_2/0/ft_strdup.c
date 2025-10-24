/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 04:28:30 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 05:29:38 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdlib.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

char    *ft_strdup(char *src)
{
    int j;
    int i;
    char *mem;

    j = 0;
    i = 0;
    while(src[i] != '\0')
    {
        i++;
    }
    mem = malloc(sizeof(char) * (i+1));
    if(!mem)
    {
        return(NULL);
    }
    while(j < i)
    {
        mem[j] = src[j];
        j++;
    } 
    mem[j] = '\0';
    return(mem);
}