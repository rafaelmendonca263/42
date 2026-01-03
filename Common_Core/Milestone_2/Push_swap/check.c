/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:56:07 by rmedonca          #+#    #+#             */
/*   Updated: 2025/12/17 16:45:41 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	help_check(int argc, char *argv[])
{
	int	i;
	int	p;

	i = 1;
	if (argc == 1)
		return (0);
	while (i < argc)
	{
		p = 0;
		while (argv[i][p])
		{
            if(p == 0 && (argv[i][p] == '+' || argv[i][p] == '-'))
                p++;
			if (ft_isdigit(argv[i][p]) == 0)
				return (-1);
			p++;
		}
		i++;
	}
	return (1);
}

int	check(int argc, char *argv[])
{
	int	i;
	int	p;

	i = help_check(argc, argv);
	if (i == 0)
		return (0);
	else if (i == -1)
		return (ft_printf("Error\n"), -1);
	i = 1;
	while (i < argc)
	{
		p = i + 1;
		while (p < argc)
		{
			if (ft_strncmp(argv[i], argv[p], ft_strlen(argv[i]) + 1) == 0)
			{
				return(ft_printf("Error\n"), -1);
			}
			p++;
		}
		i++;
	}
	return (1);
}
