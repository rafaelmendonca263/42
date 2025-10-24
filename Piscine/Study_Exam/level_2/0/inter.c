/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   inter.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 05:32:58 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 16:58:27 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int main(int argc, char **argv)
{
    int i;
    int j;

    i = 0;
    if(argc != 3)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[1][i] != '\0')
    {
        j = 0;
        while(argv[2][j] != '\0')
        {
            if(argv[1][i] == argv[2][j])
            {
                ft_putchar(argv[1][i]);
                break;
            }
            j++;
        }
        i++;
    }
    ft_putchar('\n');
}
