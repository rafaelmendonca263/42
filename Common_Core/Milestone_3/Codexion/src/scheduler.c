/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:25:02 by rmedonca          #+#    #+#             */
/*   Updated: 2026/09/24 17:43:34 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>

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
		if (pq->mode == 0
			&& pq->items[index].arrival >= pq->items[parent].arrival)
			break ;
		if (pq->mode != 0
			&& pq->items[index].deadline >= pq->items[parent].deadline)
			break ;
		temp = pq->items[index];
		pq->items[index] = pq->items[parent];
		pq->items[parent] = temp;
		index = parent;
	}
	return (0);
}

static int	get_smallest_child(t_pq *pq, int index, int left, int right)
{
	int	smallest;

	smallest = index;
	if (pq->mode == 0)
	{
		if (left < pq->size
			&& pq->items[left].arrival < pq->items[smallest].arrival)
			smallest = left;
		if (right < pq->size
			&& pq->items[right].arrival < pq->items[smallest].arrival)
			smallest = right;
	}
	else
	{
		if (left < pq->size
			&& pq->items[left].deadline < pq->items[smallest].deadline)
			smallest = left;
		if (right < pq->size
			&& pq->items[right].deadline < pq->items[smallest].deadline)
			smallest = right;
	}
	return (smallest);
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
