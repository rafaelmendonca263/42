/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   repeat_alpha.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/19 19:52:40 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/19 21:21:54 by rmedonca         ###   ########.fr       */
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
    int times;
    int times_count;

    i = 0;
    if(argc != 2)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[1][i] != '\0')
    {
        times_count = 0;
        if(argv[1][i] >= 'a' && argv[1][i] <= 'z')
        {
            times = argv[1][i] - 97;
            while(times_count <= times)
            {
                ft_putchar(argv[1][i]);
                times_count++;
            }
        }
        else if(argv[1][i] >= 'A' && argv[1][i] <= 'Z')
        {
             times = argv[1][i] - 65;
            while(times_count <= times)
            {
                ft_putchar(argv[1][i]);
                times_count++;
            }
        }
        else
        {
            ft_putchar(argv[1][i]);
        }
        i++;
    }
    ft_putchar('\n');
}