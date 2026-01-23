/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_rotate_b.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 00:41:38 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/15 16:50:23 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rrb(t_stack *b)
{
	if (!b || b->top == NULL || b->size < 2)
		return ;
	b->top = b->top->previous;
	write(1, "rrb\n", 4);
}
