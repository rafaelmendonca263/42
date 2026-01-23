/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   build_stack_a.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 08:40:08 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 14:15:18 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	add_numbers_from_arg(t_stack *a, char *arg)
{
	char	**numbers;
	int		j;
	long	num;

	numbers = ft_split(arg, ' ');
	if (!numbers)
		exit_with_error(a, NULL, NULL, numbers);
	j = 0;
	while (numbers[j])
	{
		if (numbers[j][0] == '\0')
		{
			j++;
			continue ;
		}
		num = ft_atol(numbers[j]);
		if (!ps_lstadd_back(a, (int)num))
			exit_with_error(a, NULL, NULL, numbers);
		j++;
	}
	clean(NULL, NULL, NULL, numbers);
}

int	build_stack_a(t_stack *a, int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		add_numbers_from_arg(a, argv[i]);
		i++;
	}
	return (1);
}
