/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   do_op.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 01:42:50 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/03 01:56:52 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char *argv[])
{
	int	i;

	i = 0;
	if (argc != 4)
	{
		printf("\n");
		return (0);
	}
	if (argv[2][0] == '+')
		printf("%d", atoi(argv[1]) + atoi(argv[3]));
	else if (argv[2][0] == '-')
		printf("%d", atoi(argv[1]) - atoi(argv[3]));
	else if (argv[2][0] == '*')
		printf("%d", atoi(argv[1]) * atoi(argv[3]));
	else if (argv[2][0] == '/')
		printf("%d", atoi(argv[1]) / atoi(argv[3]));
	else if (argv[2][0] == '%')
		printf("%d", atoi(argv[1]) % atoi(argv[3]));
	printf("\n");
	return (0);
}
