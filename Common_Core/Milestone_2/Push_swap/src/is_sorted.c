/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   is_sorted.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/17 17:06:05 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 14:21:45 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack *stack)
{
	t_node	*cur;

	if (!stack || stack->size < 2)
		return (1);
	cur = stack->top;
	while (cur->next != stack->top)
	{
		if (cur->content > cur->next->content)
			return (0);
		cur = cur->next;
	}
	return (1);
}
