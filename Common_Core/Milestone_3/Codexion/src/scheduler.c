/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdlib.h>
#include <string.h>

#define PQ_CMP(pq,a,b) \
	((pq)->mode == 0 ? \
		((a).arrival < (b).arrival ? -1 : ((a).arrival > (b).arrival ? 1 : ((a).id - (b).id))) \
		: ((a).deadline < (b).deadline ? -1 : ((a).deadline > (b).deadline ? 1 : ((a).arrival < (b).arrival ? -1 : ((a).arrival > (b).arrival ? 1 : ((a).id - (b).id))))))

t_pq *pq_create(int mode)
{
	t_pq *pq = malloc(sizeof(t_pq));
	if (!pq) return NULL;
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

void pq_free(t_pq *pq)
{
	if (!pq) return;
	free(pq->items);
	free(pq);

}

int pq_push(t_pq *pq, t_pq_item item)
{
	if (!pq) return -1;

	if (pq->size + 1 > pq->capacity)
	{
		int nc = pq->capacity * 2;
		t_pq_item *nb = realloc(pq->items, sizeof(t_pq_item) * nc);
		if (!nb) return -1;
		pq->items = nb;
		pq->capacity = nc;

	}
	int i = pq->size++;
 pq->items[i] = item;
 while (i > 0)
	{
		int parent = (i - 1) / 2;

		if (PQ_CMP(pq, pq->items[i], pq->items[parent]) < 0)
		{
			{ t_pq_item tmp = pq->items[i];
 pq->items[i] = pq->items[parent];
 pq->items[parent] = tmp;
 }
			i = parent;
		}
		else
			break;
	}
	return (0);
}

int pq_pop(t_pq *pq, t_pq_item *out)
{
	if (!pq || pq->size == 0) return -1;
	if (out) *out = pq->items[0];
	pq->items[0] = pq->items[--pq->size];
	int i = 0;

	while (1)
	{
		int l = 2 * i + 1;
		int r = 2 * i + 2;
		int smallest = i;

		if (l < pq->size && PQ_CMP(pq, pq->items[l], pq->items[smallest]) < 0)
			smallest = l;
		if (r < pq->size && PQ_CMP(pq, pq->items[r], pq->items[smallest]) < 0)
			smallest = r;
		if (smallest == i) break;
		{ t_pq_item tmp = pq->items[i];
 pq->items[i] = pq->items[smallest];
 pq->items[smallest] = tmp;
 }
		i = smallest;
	}
	return (0);
}

int pq_peek(t_pq *pq, t_pq_item *out)
{
	if (!pq || pq->size == 0) return -1;
	if (out) *out = pq->items[0];
	return (0);

}
