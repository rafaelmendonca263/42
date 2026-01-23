/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunks.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:33:36 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/21 15:42:17 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_array(int size, int *array)
{
	int	i;
	int	j;
	int	tmp;

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

int	*put_array(t_stack *stack)
{
	int		*array;
	int		i;
	t_node	*current;

	if (!stack || !stack->top || stack->size <= 0)
		return (NULL);
	array = malloc(sizeof(int) * stack->size);
	if (!array)
		exit_with_error(stack, NULL, NULL, NULL);
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

void	assign_index(t_stack *stack, int *array)
{
	t_node	*current;
	int		i;

	current = stack->top;
	while (1)
	{
		i = 0;
		while (i < stack->size && array[i] != current->content)
			i++;
		if (i == stack->size)
			exit_with_error(stack, NULL, NULL, NULL);
		current->idx = i;
		current = current->next;
		if (current == stack->top)
			break ;
	}
}

void	chunks(t_stack *stack_a, t_stack *stack_b)
{
	int	nbr_values;
	int	*array;
	int	start;
	int	end;
	int	total;

	nbr_values = 25;
	if (stack_a->size <= 100)
		nbr_values = 20;
	array = put_array(stack_a);
	if (!array)
		exit_with_error(stack_a, stack_b, NULL, NULL);
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
