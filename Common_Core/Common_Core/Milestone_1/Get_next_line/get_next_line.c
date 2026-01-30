/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 17:19:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/19 17:33:06 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_next_line(int fd)
{
	static char	buf[BUFFER_SIZE + 1];
	char		*line;
	int			n_bytes;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	line = NULL;
	while (1)
	{
		if (!buf[0])
		{
			n_bytes = read(fd, buf, BUFFER_SIZE);
			if (n_bytes < 0)
				return (free(line), NULL);
			if (n_bytes == 0)
				return (line);
			buf[n_bytes] = '\0';
		}
		line = extract_line(line, buf);
		if (!line)
			return (NULL);
		if (ft_strchr(line, '\n'))
			return (line);
	}
}

/* #include <stdio.h>
#include <fcntl.h>

int	main(void)
{
	int     fd;
	char    *line;
	int     i;

	fd = open("a.txt", O_RDONLY);
	if (fd < 0)
	{
		perror("open");
		return (1);
	}

	i = 0;

	printf("%s", line);
	free(line);
	printf("%s", line);
	free(line);
	printf("%s", line);
	free(line);
	close(fd);
	return (0);
	while ((line = get_next_line(fd)) != NULL)
	{
		printf("%s", line);
		free(line);
	}
} */