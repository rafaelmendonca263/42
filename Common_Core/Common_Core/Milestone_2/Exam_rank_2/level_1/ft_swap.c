/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/02 18:34:10 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/02 18:40:59 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

void	ft_swap(int *a, int *b)
{
	int	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
	return ;
}

/* int	main(void)
{
	int	a;
	int	b;

	a = 10;
	b = 2;
	ft_swap(&a, &b);
	printf("A = %d\n", a);
	printf("B = %d\n", b);
} */
