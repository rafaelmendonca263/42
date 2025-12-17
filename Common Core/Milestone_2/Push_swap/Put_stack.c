/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   Put_stack.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 08:40:08 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 10:47:21 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void put_stack(int argc, char *argv[],t_stack stack_a)
{
    int i;

    i = 1;
    while(i < argc)
    {
        ft_lstadd_front(&stack_a, ft_atol(argv[i]));
        i++;
    }
    return;
}
