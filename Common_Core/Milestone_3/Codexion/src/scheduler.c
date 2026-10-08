/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 12:24:39 by rmedonca          #+#    #+#             */
/*   Updated: 2026/10/08 13:49:52 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

int	is_higher_priority(t_pq_item *a, t_pq_item *b, int mode)
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

int	get_smallest_child(t_pq *pq, int index, int left, int right)
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
