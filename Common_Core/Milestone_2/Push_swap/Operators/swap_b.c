/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_b.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 00:36:59 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/16 05:51:08 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void sb(t_stack *b)
{
    t_node *first;
    t_node *second;

    if (!b || b->size < 2)
        return;
    first = b->top;
    second = b->top->next;
    first->previous->next = second;
    first->next = second->next;
    if (first->next)
        first->next->previous = first;

    second->next = first;
    second->previous = first->previous;
    first->previous = second;
    b->top = second;

}
