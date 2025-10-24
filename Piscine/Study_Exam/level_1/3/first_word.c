/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   first_word.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 03:14:00 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 03:32:17 by rmedonca         ###   ########.fr       */
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
        i = 0;
        while(argv[1][i] != '\0'
            && (argv[1][i] == ' ' || argv[1][i] == '\t'))
        {
            i++;
        }
        while(argv[1][i] != '\0' 
            && argv[1][i] != ' ' 
            && argv[1][i] != '\t') 
        {   
            ft_putchar(argv[1][i]);
            i++;
        }
    ft_putchar('\n');
    return(0);
}
