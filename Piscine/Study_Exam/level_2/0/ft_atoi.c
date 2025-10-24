/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 04:05:27 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 04:25:33 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_atoi(const char *str)
{
    int i;
    int neg;
    int n;
    
    i = 0;
    neg = 0;
    n = 0;
    while((str[i] >= 9 && str[i] <= 13) || str[i] == ' ')
    {
        i++;
    }
    while(str[i] == '+' || str[i] == '-')
    {
        if(str[i] == '-')
        {
            neg++;
        }
        i++;
    }
    while(str[i] >= '0' && str[i] <= '9')
    {
        n = (n * 10) + str[i] - '0';
        i++;
    }
    if(!(neg % 2 == 0))
    {
        n = -n;
    }
    return (n);
}
