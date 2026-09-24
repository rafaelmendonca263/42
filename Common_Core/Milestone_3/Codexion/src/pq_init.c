/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pq_init.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:37:33 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:37:36 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>

t_pq	*pq_create(int mode)
{
	t_pq	*pq;

	pq = malloc(sizeof(*pq));
	if (!pq)
		return (NULL);
	pq->capacity = 256;
	pq->size = 0;
	pq->mode = mode;
	pq->items = malloc(sizeof(t_pq_item) * pq->capacity);
	if (!pq->items)
	{
		free(pq);
		return (NULL);
	}
	return (pq);
}

void	pq_free(t_pq *pq)
{
	if (!pq)
		return ;
	free(pq->items);
	free(pq);
}
