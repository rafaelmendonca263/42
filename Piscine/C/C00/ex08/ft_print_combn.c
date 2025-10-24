/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*    ft_print_combn.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/07 15:30:46 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/10 19:44:53 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

static void	ft_putchar(char c)
{
	write(1, &c, 1);
}

static void	ft_print_number(int *tab, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		ft_putchar(tab[i] + '0');
		i++;
	}
	if (tab[0] != (10 - n))
	{
		ft_putchar(',');
		ft_putchar(' ');
	}
}

void	ft_print_combn(int n)
{
	int	tab[10];
	int	i;

	if (n <= 0 || n >= 10)
		return ;
	i = 0;
	while (i < n)
	{
		tab[i] = i;
		i++;
	}
	while (1)
	{
		ft_print_number(tab, n);
		i = n - 1;
		while (i >= 0 && tab[i] == 9 - (n - 1 - i))
			i--;
		if (i < 0)
			break ;
		tab[i]++;
		while (++i < n)
			tab[i] = tab[i - 1] + 1;
	}
}
