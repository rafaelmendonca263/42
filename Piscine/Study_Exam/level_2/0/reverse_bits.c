/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_bits.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 18:38:26 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 19:06:39 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned char	reverse_bits(unsigned char octet)
{
	int				i;
	unsigned char	result;

	i = 0;
	result = 0;
	while (i < 8)
	{
		result = (result * 2) + (octet % 2);
		octet = octet / 2;
		i++;
	}
	return (result);
}
