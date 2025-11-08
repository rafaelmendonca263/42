/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 17:20:09 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/07 21:37:33 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	ft_strlen(char *s)
{
	int	i;

	i = 0;
	while (s && s[i])
		i++;
	return (i);
}

int	have_newline(char *s)
{
	int	i;

	i = 0;
	while (s && s[i])
	{
		if (s[i] == '\n')
			return (1);
		i++;
	}
	return (0);
}

char	*ft_strjoin(char *s1, char *s2)
{
	char	*new;
	int		i;
	int		j;

	if (!s1)
	{
		s1 = malloc(1);
		if (!s1)
			return (NULL);
		s1[0] = '\0';
	}
	new = malloc(ft_strlen(s1) + ft_strlen(s2) + 1);
	if (!new)
		return (NULL);
	i = -1;
	while (s1[++i])
		new[i] = s1[i];
	j = 0;
	while (s2[j])
		new[i++] = s2[j++];
	new[i] = '\0';
	free(s1);
	return (new);
}

void	cut_line(char *buf)
{
	int	i;
	int	j;

	i = 0;
	while (buf[i] && buf[i] != '\n')
		i++;
	if (!buf[i])
	{
		buf[0] = '\0';
		return ;
	}
	i++;
	j = 0;
	while (buf[i])
		buf[j++] = buf[i++];
	buf[j] = '\0';
}

char	*extract_until_newline(char *buf)
{
	int		i;
	char	*res;

	i = 0;
	while (buf[i] && buf[i] != '\n')
		i++;
	if (buf[i] == '\n')
		i++;
	res = malloc(i + 1);
	if (!res)
		return (NULL);
	i = 0;
	while (buf[i] && buf[i] != '\n')
	{
		res[i] = buf[i];
		i++;
	}
	if (buf[i] == '\n')
	{
		res[i] = '\n';
		i++;
	}
	res[i] = '\0';
	return (res);
}
