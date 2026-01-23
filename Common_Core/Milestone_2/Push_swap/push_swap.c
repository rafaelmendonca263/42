/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:43:16 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 12:14:46 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;

	if (argc < 2)
		return (0);
	check_arguments(argc, argv, NULL, NULL);
	stack_a = malloc(sizeof(t_stack));
	stack_b = malloc(sizeof(t_stack));
	if (!stack_a || !stack_b)
		exit_with_error(stack_a, stack_b, NULL, NULL);
	stack_a->top = NULL;
	stack_a->size = 0;
	stack_b->top = NULL;
	stack_b->size = 0;
	if (!build_stack_a(stack_a, argc, argv))
		exit_with_error(stack_a, stack_b, NULL, NULL);
	if (is_sorted(stack_a))
		just_exit(stack_a, stack_b, NULL, NULL);
	sort_all(stack_a, stack_b);
	clean(stack_a, stack_b, NULL, NULL);
	return (0);
}
