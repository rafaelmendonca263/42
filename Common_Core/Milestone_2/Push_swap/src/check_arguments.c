/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_arguments.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:56:07 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/23 14:19:09 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_valid_number(char *str)
{
	int	i;

	if (!str)
		return (0);
	i = 0;
	if (str[i] == '+' || str[i] == '-')
		i++;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (!ft_isdigit(str[i]))
			return (0);
		i++;
	}
	return (1);
}

static void	check_duplicates(long *nums, int size, t_stack *a, t_stack *b)
{
	int	i;
	int	j;

	i = 0;
	while (i < size)
	{
		j = i + 1;
		while (j < size)
		{
			if (nums[i] == nums[j])
				exit_with_error(a, b, nums, NULL);
			j++;
		}
		i++;
	}
}

static long	parse_one_arg(char *arg, t_stack *a, t_stack *b, long *nums)
{
	long	value;

	if (!is_valid_number(arg))
		exit_with_error(a, b, nums, NULL);
	value = ft_atol(arg);
	if (value > 2147483647 || value < -2147483648)
		exit_with_error(a, b, nums, NULL);
	return (value);
}

static void	parse_args(char **args, long *nums, int *index, t_stack *a)
{
	int	i;

	i = 0;
	while (args[i])
	{
		if (args[i][0] != '\0')
		{
			nums[*index] = parse_one_arg(args[i], a, NULL, nums);
			(*index)++;
		}
		i++;
	}
}

int	check_arguments(int argc, char **argv, t_stack *stack_a, t_stack *stack_b)
{
	char	**split;
	long	*nums;
	int		i;
	int		index;

	if (argc < 2)
		return (0);
	nums = malloc(sizeof(long) * 10000);
	if (!nums)
		exit_with_error(stack_a, stack_b, NULL, NULL);
	index = 0;
	i = 1;
	while (i < argc)
	{
		split = ft_split(argv[i], ' ');
		if (!split)
			exit_with_error(stack_a, stack_b, nums, NULL);
		parse_args(split, nums, &index, stack_a);
		clean(NULL, NULL, NULL, split);
		i++;
	}
	check_duplicates(nums, index, stack_a, stack_b);
	free(nums);
	return (1);
}
