/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 17:19:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/29 18:27:12 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_next_line(int fd)
{
	int		total;
	char	*buf;
	char	*buffer;

	buf = malloc(BUFFER_SIZE + 1);
	if (!buffer)
		return (NULL);
	total = read(fd, buffer, BUFFER_SIZE);
	write(fd, buf, BUFFER_SIZE);
	close(fd);
	return (NULL);
}

int	main(void)
{
	int	fd;

	fd = open("read.md", O_RDONLY);
	if (fd < 0)
		return (1);
	while (fd > 0)
	{
		fd = write(2, "Erro: falha ao abrir o ficheiro\n", 32);
		get_next_line(fd);
	}
	return (1);
}
