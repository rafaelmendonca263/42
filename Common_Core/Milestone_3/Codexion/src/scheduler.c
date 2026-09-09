/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>                 +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa            #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>

static void	swap_items(t_pq_item *a, t_pq_item *b)
{
	t_pq_item	temp;

	temp = *a;
	*a = *b;
	*b = temp;
}

t_pq	*pq_create(int mode)
{
	t_pq	*pq;

	pq = malloc(sizeof(*pq));
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
	free(pq->items);
	free(pq);
}

int	pq_push(t_pq *pq, t_pq_item item)
{
	int		parent;
	int		index;
	t_pq_item	*new_items;
	int		new_capacity;

	if (!pq)
		return (-1);
	if (pq->size + 1 > pq->capacity)
	{
		new_capacity = pq->capacity * 2;
		new_items = realloc(pq->items, sizeof(t_pq_item) * new_capacity);
		if (!new_items)
			return (-1);
		pq->items = new_items;
		pq->capacity = new_capacity;
	}
	index = pq->size;
	pq->items[index] = item;
	pq->size++;
	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (pq->mode == 0)
		{
			if (pq->items[index].arrival >= pq->items[parent].arrival)
				break ;
		}
		else if (pq->items[index].deadline >= pq->items[parent].deadline)
			break ;
		swap_items(&pq->items[index], &pq->items[parent]);
		index = parent;
	}
	return (0);
}

int	pq_pop(t_pq *pq, t_pq_item *out)
{
	int		index;
	int		left;
	int		right;
	int		smallest;

	if (!pq || pq->size == 0)
		return (-1);
	if (out)
		*out = pq->items[0];
	pq->items[0] = pq->items[pq->size - 1];
	pq->size--;
	index = 0;
	while (index < pq->size)
	{
		left = 2 * index + 1;
		right = 2 * index + 2;
		smallest = index;
		if (left < pq->size && pq->items[left].arrival < pq->items[smallest].arrival)
			smallest = left;
		if (right < pq->size && pq->items[right].arrival < pq->items[smallest].arrival)
			smallest = right;
		if (smallest == index)
			break ;
		swap_items(&pq->items[index], &pq->items[smallest]);
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
