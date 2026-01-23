/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_rotate_a.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 00:41:36 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/15 16:50:26 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rra(t_stack *a)
{
	if (!a || a->top == NULL || a->size < 2)
		return ;
	a->top = a->top->previous;
	write(1, "rra\n", 4);
}
