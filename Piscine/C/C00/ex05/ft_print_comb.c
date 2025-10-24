/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_comb.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/06 17:00:37 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/06 19:55:11 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	writer(int a, int b, int c)
{
	char	ch;

	ch = a + '0';
	write(1, &ch, 1);
	ch = b + '0';
	write(1, &ch, 1);
	ch = c + '0';
	write(1, &ch, 1);
	if (!(a == 7 && b == 8 && c == 9))
		write(1, ", ", 2);
}

void	ft_print_comb(void)
{
	int		a;
	int		b;
	int		c;

	a = 0;
	while (a <= 7)
	{
		b = a + 1;
		while (b <= 8)
		{
			c = b + 1;
			while (c <= 9)
			{
				writer(a, b, c);
				c++;
			}
			b++;
		}
		a++;
	}
}
