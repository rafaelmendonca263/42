/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/17 17:53:30 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/17 18:11:00 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	*ft_range(int min, int max)
{
	int	*arr;
	int	len;
	int	i;

	if (min >= max)
		return (NULL);
	len = max - min;
	arr = malloc(sizeof(int) * len);
	if (!arr)
		return (NULL);
	i = 0;
	while (i < len)
	{
		arr[i] = min + i;
		i++;
	}
	return (arr);
}
