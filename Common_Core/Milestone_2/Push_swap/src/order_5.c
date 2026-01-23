/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   order_5.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:26:42 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/13 14:27:05 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_min(t_stack *stack)
{
	int		min;
	t_node	*current;

	min = stack->top->content;
	current = stack->top->next;
	while (current != stack->top)
	{
		if (current->content < min)
			min = current->content;
		current = current->next;
	}
	return (min);
}

static void	bring_min_to_top(t_stack *stack, int min)
{
	int		pos;
	t_node	*current;

	pos = 0;
	current = stack->top;
	while (current->content != min)
	{
		current = current->next;
		pos++;
	}
	if (pos <= stack->size / 2)
		while (stack->top->content != min)
			ra(stack);
	else
		while (stack->top->content != min)
			rra(stack);
}

void	order_5(t_stack *stack_a, t_stack *stack_b)
{
	int	min;

	while (stack_a->size > 3)
	{
		min = find_min(stack_a);
		bring_min_to_top(stack_a, min);
		pb(stack_a, stack_b);
	}
	order_3(stack_a);
	while (stack_b->size > 0)
		pa(stack_a, stack_b);
}
