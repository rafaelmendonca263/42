/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_arguments.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:56:07 by rmedonca          #+#    #+#             */
/*   Updated: 2026/03/13 16:39:59 by rmedonca         ###   ########.fr       */
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

static long	validate_arg(char *arg)
{
	long	value;

	if (!is_valid_number(arg))
		return (2147483649);
	value = ft_atol(arg);
	if (value > 2147483647 || value < -2147483648)
		return (2147483649);
	return (value);
}

static int	process_split(char **split, long *nums, int *index)
{
	int		i;
	long	value;

	i = 0;
	while (split[i])
	{
		if (split[i][0])
		{
			value = validate_arg(split[i]);
			if (value == 2147483649)
				return (0);
			nums[*index] = value;
			(*index)++;
		}
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
			{
				free(nums);
				exit_with_error(a, b, NULL, NULL);
			}
			j++;
		}
		i++;
	}
}

int	check_arguments(int argc, char **argv, t_stack *stack_a, t_stack *stack_b)
{
	long	*nums;
	char	**split;
	int		i;
	int		index;

	nums = malloc(sizeof(long) * 10000);
	if (!nums)
		exit_with_error(stack_a, stack_b, NULL, NULL);
	index = 0;
	i = 1;
	while (i < argc)
	{
		split = ft_split(argv[i], ' ');
		if (!split || !process_split(split, nums, &index))
		{
			clean(NULL, NULL, NULL, split);
			exit_with_error(stack_a, stack_b, nums, NULL);
		}
		clean(NULL, NULL, NULL, split);
		i++;
	}
	check_duplicates(nums, index, stack_a, stack_b);
	free(nums);
	return (1);
}
