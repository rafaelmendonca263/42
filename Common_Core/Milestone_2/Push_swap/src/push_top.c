/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_top.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 01:52:32 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/16 00:18:23 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*push_top(t_stack *stack, t_node *node)
{
	if (!node)
		exit_with_error(stack, NULL, NULL, NULL);
	if (!stack->top)
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
	return (node);
}
