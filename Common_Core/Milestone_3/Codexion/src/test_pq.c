/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_pq.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafa <rafa@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/21 12:01:18 by rafa                   #+#    #+#             */
/*   Updated: 2026/08/21 12:01:18 by rafa                   ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"
#include <stdio.h>
#include <string.h>

static int test_fifo()
{
	t_pq *pq = pq_create(0);
	if (!pq) return 1;
	t_pq_item a = { .id = 1, .arrival = 100, .deadline = 0 };
	t_pq_item b = { .id = 2, .arrival = 200, .deadline = 0 };
	t_pq_item c = { .id = 3, .arrival = 150, .deadline = 0 };
	pq_push(pq, a);
	pq_push(pq, b);
	pq_push(pq, c);
	t_pq_item out;
	pq_pop(pq, &out);
	if (out.id != 1) { pq_free(pq);

 return 1;
 }
	pq_pop(pq, &out);
	if (out.id != 3) { pq_free(pq);
 return 1;
 }
	pq_pop(pq, &out);
	if (out.id != 2) { pq_free(pq);
 return 1;
 }
	pq_free(pq);
	return (0);
}

static int test_edf()
{
	t_pq *pq = pq_create(1);
	if (!pq) return 1;
	t_pq_item a = { .id = 1, .arrival = 100, .deadline = 500 };
	t_pq_item b = { .id = 2, .arrival = 200, .deadline = 300 };
	t_pq_item c = { .id = 3, .arrival = 150, .deadline = 400 };
	pq_push(pq, a);
	pq_push(pq, b);
	pq_push(pq, c);
	t_pq_item out;
	pq_pop(pq, &out);
	if (out.id != 2) { pq_free(pq);

 return 1;
 }
	pq_pop(pq, &out);
	if (out.id != 3) { pq_free(pq);
 return 1;
 }
	pq_pop(pq, &out);
	if (out.id != 1) { pq_free(pq);
 return 1;
 }
	pq_free(pq);
	return (0);
}

int main()
{
	int r1 = test_fifo();
	int r2 = test_edf();

	if (r1 == 0 && r2 == 0)
	{
		printf("PQ tests passed\n");
		return (0);

	}
	printf("PQ tests failed: fifo=%d edf=%d\n", r1, r2);
	return (1);
}
