/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   aff_a.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/19 14:16:17 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/19 16:52:58 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c,1);
}

char main(int argc, char **argv)
{
    int i;

    i = 0;
    if (argc != 2)
    {
        ft_putchar('a');
    }
    while(argv[1][i] != '\0')
    {
        if(argv[1][i] == 'a')
            ft_putchar('a');
            break;
        i++;
    }
    ft_putchar('\n');
    return(0);
}