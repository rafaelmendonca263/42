/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush04.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rparreir <rparreir@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/02 20:01:28 by rparreir          #+#    #+#             */
/*   Updated: 2025/08/03 20:43:38 by rparreir         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c);

void	horizontal_inicial(int x)
{
	int	xi;

	xi = 0;
	while (xi < x)
	{
		if (xi == 0)
			ft_putchar('A');
		else if (xi == x - 1)
			ft_putchar('C');
		else
			ft_putchar('B');
		xi++;
	}
	ft_putchar('\n');
}

void	horizontal_final(int x)
{
	int	xi;

	xi = 0;
	while (xi < x)
	{
		if (xi == 0)
			ft_putchar('C');
		else if (xi == x - 1)
			ft_putchar('A');
		else
			ft_putchar('B');
		xi++;
	}
	ft_putchar('\n');
}

void	vertical(int x)
{
	int	xi;

	xi = 0;
	while (xi < x)
	{
		if (xi == 0 || xi == x - 1)
			ft_putchar('B');
		else
			ft_putchar(' ');
		xi++;
	}
	ft_putchar('\n');
}

void	rush(int x, int y)
{
	int	yi;

	if (x <= 0 || y <= 0)
	{
		write(1, "Error\n", 6);
		return ;
	}
	yi = 0;
	while (yi < y)
	{
		if (yi == 0)
			horizontal_inicial(x);
		else if (yi == y - 1)
			horizontal_final(x);
		else
			vertical(x);
		yi++;
	}
}
