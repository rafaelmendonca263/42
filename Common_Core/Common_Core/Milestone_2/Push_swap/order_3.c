/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   order_3.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 17:38:15 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/13 17:38:16 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


void	order_3(t_stack *stack_a)
{
	int	a;
	int	b;
	int	c;

	a = stack_a->top->content;
	b = stack_a->top->next->content;
	c = stack_a->top->next->next->content;
	if (is_sorted(stack_a))
		return ;
	if ((a < b) && (b > c) && (c > a))
	{
		sa(stack_a);
		ra(stack_a);
	}
	else if ((a > b) && (b < c) && (c > a))
		sa(stack_a);
	else if ((a < b) && (b > c) && (c < a))
		rra(stack_a);
	else if ((a > b) && (b < c) && (c < a))
		ra(stack_a);
	else if ((a > b) && (b > c) && (c < a))
	{
		sa(stack_a);
		rra(stack_a);
	}
}
