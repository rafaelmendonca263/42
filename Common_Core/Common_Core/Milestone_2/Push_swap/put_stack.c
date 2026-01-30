/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   put_stack.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 08:40:08 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/13 17:53:00 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void put_stack(int argc, char *argv[],t_stack *stack_a)
{
    int i;

    i = 1;
    while(i < argc)
    {
        ft_lstadd_back(stack_a, ft_atol(argv[i]));
        i++;
    }
    return;
}
