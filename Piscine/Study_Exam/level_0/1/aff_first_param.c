/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   aff_first_param.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/19 16:57:55 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/19 18:10:32 by rmedonca         ###   ########.fr       */
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

    i = 0;
    if (argc < 2)
    {
        ft_putchar('\n');
        return(0);
    }
    else
    {
        while(argv[1][i])
        {
            ft_putchar(argv[1][i]);
            i++;
        }
        ft_putchar('\n');
    }
    return(0);
}