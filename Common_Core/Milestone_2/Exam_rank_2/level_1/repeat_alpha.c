/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   repeat_alpha.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/02 18:41:23 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/02 23:25:10 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

int	main(int argc, char *argv[])
{
	int	i;
	int	p;

	i = 0;
	if (argc != 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	while (argv[1][i])
	{
		if (argv[1][i] >= 'A' && argv[1][i] <= 'Z')
		{
			p = 0;
			while (p <= (argv[1][i] - 65))
			{
				ft_putchar(argv[1][i]);
				p++;
			}
		}
		else if (argv[1][i] >= 'a' && argv[1][i] <= 'z')
		{
			p = 0;
			while (p <= (argv[1][i] - 97))
			{
				ft_putchar(argv[1][i]);
				p++;
			}
		}
		else
			ft_putchar(argv[1][i]);
		i++;
	}
	ft_putchar('\n');
	return (0);
}
