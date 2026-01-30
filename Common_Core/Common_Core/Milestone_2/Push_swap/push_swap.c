/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:43:16 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/13 12:28:06 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char *argv[])
{
	t_stack	stack_a;
	t_stack	stack_b;

	stack_a.top = NULL;
	stack_a.size = 0;
	stack_b.top = NULL;
	stack_b.size = 0;
	if (check(argc, argv) != 1)
		return (1);
	put_stack(argc, argv, &stack_a);
	if(is_sorted(stack_a))
	return (0);
	if(size == 2)
		sa(stack_a);
	else if(size == 3)
		order_3(stack_a);
	else if( <= 5)
		order_5(stack_a);
	else
		
}
