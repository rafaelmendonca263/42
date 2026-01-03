/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 17:20:09 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/19 17:02:58 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*append_buffer(char *line, char *buf, int len)
{
	char	*new_line;
	int		i;
	int		j;

	i = 0;
	while (line && line[i])
		i++;
	new_line = malloc(i + len + 1);
	if (!new_line)
		return (free(line), NULL);
	j = 0;
	while (j < i)
	{
		new_line[j] = line[j];
		j++;
	}
	i = 0;
	while (i < len)
	{
		new_line[j + i] = buf[i];
		i++;
	}
	new_line[j + i] = '\0';
	free(line);
	return (new_line);
}

char	*ft_strchr(char *s, int c)
{
	int	i;

	if (!s)
		return (NULL);
	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return (&s[i]);
		i++;
	}
	return (NULL);
}

int	ft_strlen(char *s)
{
	int	i;

	i = 0;
	while (s && s[i])
		i++;
	return (i);
}

char	*extract_line(char *line, char *buf)
{
	int	i;
	int	j;

	i = 0;
	while (buf[i] && buf[i] != '\n')
		i++;
	if (buf[i] == '\n')
		i++;
	line = append_buffer(line, buf, i);
	if (!line)
		return (NULL);
	j = 0;
	while (buf[i])
	{
		buf[j] = buf[i];
		j++;
		i++;
	}
	buf[j] = '\0';
	return (line);
}
