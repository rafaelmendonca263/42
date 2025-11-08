/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 13:31:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/29 18:53:05 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/// @brief Works similar to ft_strlen but for lists.
/// @param lst
/// @return i
int	ft_lstsize(t_list *lst)
{
	size_t	i;

	i = 0;
	while (lst != NULL)
	{
		i++;
		lst = lst->next;
	}
	return (i);
}

/* int	main(void)
{
	t_list *a = ft_lstnew("primeiro");
	t_list *b = ft_lstnew("segundo");
	t_list *c = ft_lstnew("terceiro");

	a->next = b;
	b->next = c;
	printf("Tamanho da lista: %d\n", ft_lstsize(a));
	return (0);
} */