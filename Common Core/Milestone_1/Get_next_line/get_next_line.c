/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 17:19:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/07 21:36:24 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	fill_buf(int fd, char *buf)
{
	int	b;

	b = read(fd, buf, BUFFER_SIZE);
	if (b <= 0)
	{
		buf[0] = '\0';
		return (b);
	}
	buf[b] = '\0';
	return (b);
}

char	*append_line(char *line, char *buf)
{
	char	*temp;

	temp = extract_until_newline(buf);
	line = ft_strjoin(line, temp);
	free(temp);
	return (line);
}

char	*get_next_line(int fd)
{
	static char	buf[BUFFER_SIZE + 1];
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	line = NULL;
	while (1)
	{
		if (!buf[0] && fill_buf(fd, buf) <= 0)
		{
			if (!line || !line[0])
				return (free(line), NULL);
			break ;
		}
		line = append_line(line, buf);
		if (have_newline(buf))
		{
			cut_line(buf);
			break ;
		}
		buf[0] = '\0';
	}
	return (line);
}
