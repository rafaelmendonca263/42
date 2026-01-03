/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pop_top.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 01:52:32 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/16 02:17:53 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*push_top(t_stack *stack, t_node *node)
{
	if (!node)
		return;
	if(!stack->top)
	{
		node->next = node;
		node->previous = node;
		stack->top = node;
	}
	else
	{
		node->next = stack->top;
        node->previous = stack->top->previous;
        stack->top->previous->next = node;
        stack->top->previous = node;
        stack->top = node;
	}
	stack->size++;
}
