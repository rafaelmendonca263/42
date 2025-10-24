/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   first_word.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/20 21:51:29 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 03:14:54 by rmedonca         ###   ########.fr       */
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
        if(argv[1][i] == ' ' || argv[1][i] == 9)
        {
            i++;
        }
        else if(argv[1][i] >= '!' && argv[1][i] <= '~') 
        {
            ft_putchar(argv[1][i]);
            if(argv[1][i+1] == ' ' || argv[1][i+1] == 9)
            {
                break;
            }
            i++;
        }
    }
    ft_putchar('\n');
    return(0);
}
