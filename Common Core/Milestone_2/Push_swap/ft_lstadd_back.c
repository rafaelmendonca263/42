/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 13:28:54 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 17:00:50 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Add node on the final of the list
/// @param lst
/// @param
void	ft_lstadd_back(t_stack *stack, int i)
{
	t_node	*node;

	if (!stack)
		return ;
	node = malloc(sizeof(t_node));
	if (!node)
		return ;
	node->content = i;
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
}
