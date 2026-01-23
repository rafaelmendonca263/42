/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   order_less_than_five.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 18:42:02 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 09:18:51 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	order_less_than_five(t_stack *stack_a, t_stack *stack_b)
{
	if (stack_a->size == 2)
		ra(stack_a);
	else if (stack_a->size == 3)
		order_3(stack_a);
	else if ((stack_a->size > 3) && (stack_a->size <= 5))
		order_5(stack_a, stack_b);
}
