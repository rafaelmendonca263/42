/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/20 23:57:03 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 00:01:52 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

void	ft_putstr(char *str)
{
    int i;
    
    i = 0;
    while(str[i] != '\0')
    {    
        ft_putchar(str);
        i++;
    }
}
