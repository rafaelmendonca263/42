/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_program_name.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/13 16:03:04 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/19 12:03:40 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

int	main(int argc, char **argv)
{
	int	i;

	if (argc >= 1)
	{
		i = 0;
		while (argv[0][i] != '\0')
		{
			ft_putchar (argv[0][i]);
			i++;
		}
		ft_putchar ('\n');
	}
	return (0);
}
