/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_to_b.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 09:40:23 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/14 12:23:50 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_pos_in_chunk(t_stack *stack, int start, int end)
{
	t_node	*current;
	int		pos;

	current = stack->top;
	pos = 0;
	while (1)
	{
		if (current->idx >= start && current->idx < end)
			return (pos);
		current = current->next;
		pos++;
		if (current == stack->top)
			break ;
	}
	return (-1);
}

static void	move_to_chunk_top(t_stack *stack, int start, int end)
{
	int	pos;

	pos = find_pos_in_chunk(stack, start, end);
	if (pos == -1)
		return ;
	if (pos <= stack->size / 2)
		ra(stack);
	else
		rra(stack);
}

void	push_chunk(t_stack *stack_a, t_stack *stack_b, int start, int end)
{
	int	moved;
	int	chunk_size;

	moved = 0;
	chunk_size = end - start;
	while (moved < chunk_size && stack_a->size > 0)
	{
		if (stack_a->top->idx >= start && stack_a->top->idx < end)
		{
			pb(stack_a, stack_b);
			if (stack_b->top->idx < (start + end) / 2)
				rb(stack_b);
			moved++;
		}
		else
			move_to_chunk_top(stack_a, start, end);
	}
}
