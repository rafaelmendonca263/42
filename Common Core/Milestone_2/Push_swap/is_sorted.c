/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   is_sorted.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/17 17:06:05 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 18:27:47 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	get_order(t_stack *stack)
{
	t_node	*cur;
	int		asc;
	int		desc;

	asc = 1;
	desc = 1;
	if (stack->size < 2)
		return (1);
	cur = stack->top;
	while (cur->next != stack->top)
	{
		if (cur->content > cur->next->content)
			asc = 0;
		if (cur->content < cur->next->content)
			desc = 0;
		cur = cur->next;
	}
	if (asc)
		return (1);
	if (desc)
		return (2);
	return (0);
}
