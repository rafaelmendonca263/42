/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 13:29:42 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 17:01:03 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Add the node in the begining of the list
/// @param lst
/// @param
void	ft_lstadd_front(t_stack *stack, int i)
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
		node->next = node;
		node->previous = node;
	}
	else
	{
		node->next = stack->top;
		node->previous = stack->top->previous;
		stack->top->previous = node;
		node->previous->next = node;
		stack->top = node;
	}
	stack->size++;
}
