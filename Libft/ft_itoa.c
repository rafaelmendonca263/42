/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 18:59:56 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/28 13:28:43 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	nmb_len(int n)
{
	int	size;

	size = (n <= 0);
	while (n != 0)
	{
		n /= 10;
		size++;
	}
	return (size);
}

/// @brief Integer to Ascii.
/// @param n
/// @return ptr
char	*ft_itoa(int n)
{
	char	*ptr;
	int		size;
	long	num;

	if (n == -2147483648)
		return (ft_strdup("-2147483648"));
	num = n;
	if (n < 0)
		num = -num;
	if (n == 0)
		return (ft_strdup("0"));
	size = nmb_len(n);
	ptr = malloc(sizeof(char) * (size + 1));
	if (!ptr)
		return (NULL);
	ptr[size--] = '\0';
	while (num > 0)
	{
		ptr[size--] = (num % 10) + '0';
		num /= 10;
	}
	if (n < 0)
		ptr[0] = '-';
	return (ptr);
}
