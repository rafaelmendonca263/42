/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alpha_mirror.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 00:53:04 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/03 01:21:47 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

int	main(int argc, char *argv[])
{
	int i;

	i = 0;
	if (argc != 2)
	{
		write(1, "\n", 1);
		return (0);
	}
	while (argv[1][i])
	{
		if (argv[1][i] >= 'A' && argv[1][i] <= 'M')
			ft_putchar(90 - (argv[1][i] - 65));
		else if (argv[1][i] >= 'a' && argv[1][i] <= 'm')
			ft_putchar(122 - (argv[1][i] - 97));
		else if (argv[1][i] >= 'N' && argv[1][i] <= 'Z')
			ft_putchar(90 - (argv[1][i] - 65));
		else if (argv[1][i] >= 'n' && argv[1][i] <= 'z')
			ft_putchar(122 - (argv[1][i] - 97));
		else
			ft_putchar(argv[1][i]);
		i++;
	}
	ft_putchar('\n');
	return (0);
}