/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunks.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:33:36 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/13 18:30:01 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdlib.h>

int	*put_array(t_stack *stack)
{
	int		*array;
	int		i;
	t_node	*current;

	array = malloc(sizeof(int) * stack->size);
	if (!array)
		return (NULL);
	current = stack->top;
	i = 0;
	while (i < stack->size)
	{
		array[i] = current->content;
		current = current->next;
		i++;
	}
	sort_array(stack->size, array);
	return (array);
}

void	sort_array(int size, int *array)
{
	int i, j, tmp;
	i = 0;
	while (i < size - 1)
	{
		j = i + 1;
		while (j < size)
		{
			if (array[i] > array[j])
			{
				tmp = array[i];
				array[i] = array[j];
				array[j] = tmp;
			}
			j++;
		}
		i++;
	}
}

void	assign_index(t_stack *stack, int *array)
{
	t_node	*current;
	int		i;

	current = stack->top;
	while (1)
	{
		i = 0;
		while (array[i] != current->content)
			i++;
		current->index = i;
		current = current->next;
		if (current == stack->top)
			break ;
	}
}

void	push_chunk(t_stack *stack_a, t_stack *stack_b, int start, int end)
{
	int	moved;
	int	chunk_size;

	moved = 0;
	chunk_size = end - start;
	while (moved < chunk_size && stack_a->size > 0)
	{
		if (stack_a->top->index >= start && stack_a->top->index < end)
		{
			pb(stack_a, stack_b);
			if (stack_b->top->index < (start + end) / 2)
				rb(stack_b);
			moved++;
		}
		else
			ra(stack_a);
	}
}

void	chunks(t_stack *stack_a, t_stack *stack_b)
{
	int	nbr_values;
	int	*array;
	int	start;
	int	end;
	int	total;

	nbr_values = (stack_a->size <= 100) ? 20 : 25;
	array = put_array(stack_a);
	if (!array)
		return ;
	assign_index(stack_a, array);
	total = stack_a->size;
	start = 0;
	end = nbr_values;
	while (start < total)
	{
		if (end > total)
			end = total;
		push_chunk(stack_a, stack_b, start, end);
		start = end;
		end += nbr_values;
	}
	free(array);
}
