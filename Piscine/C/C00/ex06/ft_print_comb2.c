/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_comb2.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/06 19:25:44 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/06 21:47:15 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	writer(int ab, int cd)
{
	ft_putchar((ab / 10) + '0');
	ft_putchar((ab % 10) + '0');
	ft_putchar(' ');
	ft_putchar((cd / 10) + '0');
	ft_putchar((cd % 10) + '0');
	if (!(ab == 98 && cd == 99))
	{
		ft_putchar(',');
		ft_putchar(' ');
	}
}

void	ft_print_comb2(void)
{
	int		ab;
	int		cd;

	ab = 0;
	while (ab <= 98)
	{
		cd = ab + 1;
		while (cd <= 99)
		{
			writer(ab, cd);
			cd++;
		}
		ab++;
	}
}
