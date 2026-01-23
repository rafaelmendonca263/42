/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_back_to_a.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 09:44:30 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/15 16:54:06 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_max_index(t_stack *stack)
{
	t_node	*current;
	int		max;

	current = stack->top;
	max = current->idx;
	current = current->next;
	while (current != stack->top)
	{
		if (current->idx > max)
			max = current->idx;
		current = current->next;
	}
	return (max);
}

static int	find_pos_index(t_stack *stack, int idx)
{
	t_node	*current;
	int		pos;

	current = stack->top;
	pos = 0;
	while (1)
	{
		if (current->idx == idx)
			return (pos);
		current = current->next;
		pos++;
		if (current == stack->top)
			break ;
	}
	return (-1);
}

static void	move_max_to_top(t_stack *stack)
{
	int	max;
	int	pos;

	max = find_max_index(stack);
	pos = find_pos_index(stack, max);
	if (pos <= stack->size / 2)
	{
		while (stack->top->idx != max)
			rb(stack);
	}
	else
	{
		while (stack->top->idx != max)
			rrb(stack);
	}
}

void	push_back_to_a(t_stack *stack_a, t_stack *stack_b)
{
	while (stack_b->size > 0)
	{
		move_max_to_top(stack_b);
		pa(stack_a, stack_b);
	}
}
