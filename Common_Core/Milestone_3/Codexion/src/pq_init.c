/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pq_init.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:36 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 13:01:13 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

t_pq	*pq_create(int mode)
{
	t_pq	*pq;

	pq = malloc(sizeof(t_pq));
	if (!pq)
		return (NULL);
	pq->capacity = 16;
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
	if (pq->items)
		free(pq->items);
	free(pq);
}

int	pq_push(t_pq *pq, t_pq_item item)
{
	int			parent;
	int			index;
	t_pq_item	temp;

	if (!pq || pq->size + 1 > pq->capacity)
		return (-1);
	index = pq->size;
	pq->items[index] = item;
	pq->size++;
	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!is_higher_priority(&pq->items[index],
				&pq->items[parent], pq->mode))
			break ;
		temp = pq->items[index];
		pq->items[index] = pq->items[parent];
		pq->items[parent] = temp;
		index = parent;
	}
	return (0);
}

int	pq_pop(t_pq *pq, t_pq_item *out)
{
	int			index;
	int			smallest;
	t_pq_item	temp;

	if (!pq || pq->size == 0)
		return (-1);
	if (out)
		*out = pq->items[0];
	pq->items[0] = pq->items[pq->size - 1];
	pq->size--;
	index = 0;
	while (index < pq->size)
	{
		smallest = get_smallest_child(pq, index, 2 * index + 1, 2 * index + 2);
		if (smallest == index)
			break ;
		temp = pq->items[index];
		pq->items[index] = pq->items[smallest];
		pq->items[smallest] = temp;
		index = smallest;
	}
	return (0);
}

int	pq_peek(t_pq *pq, t_pq_item *out)
{
	if (!pq || pq->size == 0)
		return (-1);
	if (out)
		*out = pq->items[0];
	return (0);
}
