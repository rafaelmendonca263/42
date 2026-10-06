/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pq_init.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/24 17:25:02 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/06 16:28:26 by rafa             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	is_higher_priority(t_pq_item *a, t_pq_item *b, int mode)
{
	if (mode == 0)
	{
		if (a->arrival != b->arrival)
			return (a->arrival < b->arrival);
		return (a->id < b->id);
	}
	if (a->deadline != b->deadline)
		return (a->deadline < b->deadline);
	if (a->arrival != b->arrival)
		return (a->arrival < b->arrival);
	return (a->id < b->id);
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

static int	get_smallest_child(t_pq *pq, int index, int left, int right)
{
	int	smallest;

	smallest = index;
	if (left < pq->size
		&& is_higher_priority(&pq->items[left],
			&pq->items[smallest], pq->mode))
		smallest = left;
	if (right < pq->size
		&& is_higher_priority(&pq->items[right],
			&pq->items[smallest], pq->mode))
		smallest = right;
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
