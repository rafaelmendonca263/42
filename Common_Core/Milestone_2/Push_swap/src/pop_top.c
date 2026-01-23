/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pop_top.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 01:50:16 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/16 00:19:09 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*pop_top(t_stack *stack)
{
	t_node	*node;

	if (!stack || !stack->top)
		exit_with_error(stack, NULL, NULL, NULL);
	node = stack->top;
	if (stack->size == 1)
	{
		stack->top = NULL;
	}
	else
	{
		node->previous->next = node->next;
		node->next->previous = node->previous;
		stack->top = node->next;
	}
	node->next = NULL;
	node->previous = NULL;
	stack->size--;
	return (node);
}
