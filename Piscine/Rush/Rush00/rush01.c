/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush01.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/03 17:41:46 by rparreir          #+#    #+#             */
/*   Updated: 2025/08/04 17:02:53 by rmedonca         ###   ########.fr       */
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
			ft_putchar('/');
		else if (xi == x - 1 && x != 1)
			ft_putchar('\\');
		else
			ft_putchar('*');
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
			ft_putchar('\\');
		else if (xi == x - 1)
			ft_putchar('/');
		else
			ft_putchar('*');
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
			ft_putchar('*');
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
