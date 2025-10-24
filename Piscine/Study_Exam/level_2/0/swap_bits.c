/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_bits.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/21 19:08:49 by rmedonca          #+#    #+#             */
/*   Updated: 2025/08/21 19:17:18 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

unsigned char	swap_bits(unsigned char octet)
{
    unsigned char high;
    unsigned char low;

    high = octet / 16;
    low = octet % 16;

    return (low * 16 + high);
}
