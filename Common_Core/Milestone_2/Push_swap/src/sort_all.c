/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_all.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/22 00:54:42 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/22 00:57:31 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_all(t_stack *stack_a, t_stack *stack_b)
{
	if (stack_a->size <= 5)
		order_less_than_five(stack_a, stack_b);
	else
	{
		chunks(stack_a, stack_b);
		push_back_to_a(stack_a, stack_b);
	}
}
