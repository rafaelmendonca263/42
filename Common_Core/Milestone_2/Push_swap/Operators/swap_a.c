/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_a.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 00:36:49 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/16 05:50:23 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void sa(t_stack *a)
{
    t_node *first;
    t_node *second;

    if (!a || a->size < 2)
        return;
    first = a->top;
    second = a->top->next;
    first->previous->next = second;
    first->next = second->next;
    if (first->next)
        first->next->previous = first;

    second->next = first;
    second->previous = first->previous;
    first->previous = second;
    a->top = second;
}
