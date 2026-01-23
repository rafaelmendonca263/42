/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clean_and_exit.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 20:54:09 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 09:49:00 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	free_stack(t_stack *stack)
{
	t_node	*cur;
	t_node	*next;

	if (!stack || !stack->top)
		return ;
	cur = stack->top->next;
	while (cur != stack->top)
	{
		next = cur->next;
		free(cur);
		cur = next;
	}
	free(stack->top);
	stack->top = NULL;
	stack->size = 0;
}

void	clean(t_stack *a, t_stack *b, long *nums, char **words)
{
	int	i;

	if (words)
	{
		i = 0;
		while (words[i])
			free(words[i++]);
		free(words);
	}
	if (nums)
		free(nums);
	if (a)
	{
		free_stack(a);
		free(a);
	}
	if (b)
	{
		free_stack(b);
		free(b);
	}
}

void	just_exit(t_stack *a, t_stack *b, long *nums, char **words)
{
	clean(a, b, nums, words);
	exit(0);
}

void	exit_with_error(t_stack *a, t_stack *b, long *nums, char **words)
{
	write(2, "Error\n", 6);
	clean(a, b, nums, words);
	exit(1);
}
