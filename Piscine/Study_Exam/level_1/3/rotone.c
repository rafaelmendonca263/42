/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotone.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 03:52:22 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 04:03:07 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int main(int argc, char *argv[])
{
    int i;

    i = 0;
    if(argc != 2)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[1][i] != '\0')
    {
        if((argv[1][i] >= 'a' && argv[1][i] <= 'y') 
        || (argv[1][i] >= 'A' && argv[1][i] <= 'Y'))
        {
            ft_putchar(argv[1][i] + 1);
        }
        else if(argv[1][i] == 'z' || argv[1][i] == 'Z')
        {
            ft_putchar(argv[1][i] - 25);
        }
        else
        {
            ft_putchar(argv[1][i]);
        }
        i++;
    }
    ft_putchar('\n');
}