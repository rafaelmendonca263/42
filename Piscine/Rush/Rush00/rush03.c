/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush03.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/02 20:01:24 by rparreir          #+#    #+#             */
/*   Updated: 2025/08/04 17:00:40 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c);

void	horizontal(int x)
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

void	vertical(int x)
{
	int	i;

	if (x == 1)
	{
		ft_putchar('B');
	}
	else
	{
		ft_putchar('B');
		i = 0;
		while (i < x - 2)
		{
			ft_putchar(' ');
			i++;
		}
		ft_putchar('B');
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
		if (yi == 0 || yi == y - 1)
			horizontal(x);
		else
			vertical(x);
		yi++;
	}
}
