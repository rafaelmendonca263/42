/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 00:32:35 by rmedonca          #+#    #+#             */
/*   Updated: 2026/03/13 16:33:19 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "ft_printf.h"
# include "libft.h"
# include <limits.h>
# include <stdarg.h>
# include <stddef.h>
# include <stdio.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_node
{
	int				content;
	int				idx;
	struct s_node	*next;
	struct s_node	*previous;
}					t_node;

typedef struct s_stack
{
	t_node			*top;
	int				size;
}					t_stack;

// Lists
void				ps_lstadd_front(t_stack *stack, int i);
t_node				*push_top(t_stack *stack, t_node *node);
t_node				*pop_top(t_stack *stack);
int					ps_lstadd_back(t_stack *stack, int i);

// Helper
int					check_arguments(int argc, char **argv, t_stack *stack_a,
						t_stack *stack_b);
void				push_chunk(t_stack *stack_a, t_stack *stack_b, int start,
						int end);
int					is_sorted(t_stack *stack);
void				order_3(t_stack *stack_a);
void				order_5(t_stack *stack_a, t_stack *stack_b);
void				chunks(t_stack *stack_a, t_stack *stack_b);
int					build_stack_a(t_stack *a, int argc, char **argv);
void				push_back_to_a(t_stack *stack_a, t_stack *stack_b);
void				order_5(t_stack *stack_a, t_stack *stack_b);
void				order_less_than_five(t_stack *a, t_stack *b);
void				sort_all(t_stack *stack_a, t_stack *stack_b);

// Operaters push_swap
void				sa(t_stack *a);
void				sb(t_stack *b);
void				ss(t_stack *a, t_stack *b);
void				pa(t_stack *a, t_stack *b);
void				pb(t_stack *a, t_stack *b);
void				ra(t_stack *a);
void				rb(t_stack *b);
void				rr(t_stack *a, t_stack *b);
void				rra(t_stack *a);
void				rrb(t_stack *b);
void				rrr(t_stack *a, t_stack *b);

// Clean
void				exit_with_error(t_stack *a, t_stack *b, long *nums,
						char **words);
void				clean(t_stack *a, t_stack *b, long *nums, char **words);
void				just_exit(t_stack *a, t_stack *b, long *nums, char **words);

// Tester
void				print_stack(t_node *head_a, t_node *head_b);

#endif