/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi_base.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/11 11:39:51 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/13 14:56:45 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	ft_strlen(char *base)
{
	int	i;

	i = 0;
	while (base[i] != '\0')
		i++;
	return (i);
}

int	confirm_base(char *base)
{
	int	i;
	int	j;

	i = 0;
	while (base[i] != '\0')
	{
		if (base[i] == '-' || base[i] == '+'
			|| (base[i] >= 9 && base[i] <= 13) || base[i] == ' ')
			return (0);
		j = i + 1;
		while (base[j] != '\0')
		{
			if (base[i] == base[j])
				return (0);
			j++;
		}
		i++;
	}
	if (i < 2)
		return (0);
	return (1);
}

int	char_in_base(char c, char *base)
{
	int	j;

	j = 0;
	while (base[j] != '\0')
	{
		if (base[j] == c)
			return (j);
		j++;
	}
	return (-1);
}

int	skip_spaces_and_signs(char *str, int *i)
{
	int	neg;

	neg = 0;
	while ((str[*i] >= 9 && str[*i] <= 13) || str[*i] == ' ')
		(*i)++;
	while (str[*i] == '+' || str[*i] == '-')
		if (str[(*i)++] == '-')
			neg++;
	return (neg);
}

int	ft_atoi_base(char *str, char *base)
{
	int	i;
	int	neg;
	int	res;
	int	base_len;
	int	index;

	i = 0;
	res = 0;
	base_len = ft_strlen(base);
	if (!confirm_base(base))
		return (0);
	neg = skip_spaces_and_signs(str, &i);
	index = char_in_base(str[i], base);
	while (index != -1)
	{
		res = res * base_len + index;
		i++;
		index = char_in_base(str[i], base);
	}
	if (neg % 2)
		res = -res;
	return (res);
}

/*int	main(void)
{
	printf("%d\n", ft_atoi_base(" ---+--+1234ab567", "0123456789"));
	printf("%d\n", ft_atoi_base("   \t\n+2A", "0123456789ABCDEF"));
	printf("%d\n", ft_atoi_base("--1010", "01"));  
	printf("%d\n", ft_atoi_base("  -+ 123", "0123456789"));     
	printf("%d\n", ft_atoi_base("poney", "poneyvif"));
*/