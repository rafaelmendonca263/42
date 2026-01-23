/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 13:28:54 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 14:22:04 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Add node on the final of the list
/// @param lst
/// @param
int	ps_lstadd_back(t_stack *stack, int i)
{
	t_node	*node;

	if (!stack)
		exit_with_error(stack, NULL, NULL, NULL);
	node = malloc(sizeof(t_node));
	if (!node)
		exit_with_error(stack, NULL, NULL, NULL);
	node->content = i;
	node->idx = 0;
	if (stack->size == 0)
	{
		stack->top = node;
		node->next = node;
		node->previous = node;
	}
	else
	{
		node->next = stack->top;
		node->previous = stack->top->previous;
		node->previous->next = node;
		stack->top->previous = node;
	}
	stack->size++;
	return (1);
}
