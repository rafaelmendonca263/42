/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   search_and_replace.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/19 21:23:59 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/19 21:50:10 by rmedonca         ###   ########.fr       */
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

	i = 0;
	if (argc != 4 || argv[2][1] != '\0' || argv[3][1] != '\0')
	{
		ft_putchar('\n');
		return (0);
	}
	while (argv[1][i] != '\0')
	{
		if (argv[1][i] == argv[2][0])
			ft_putchar(argv[3][0]);
		else
			ft_putchar(argv[1][i]);
		i++;
	}
	ft_putchar('\n');
	return (0);
}
