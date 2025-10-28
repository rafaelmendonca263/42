/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 18:59:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/28 14:55:11 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	count_words(const char *s, char c)
{
	int	i;
	int	count;

	i = 0;
	count = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (s[i] && s[i] != c)
			count++;
		while (s[i] && s[i] != c)
			i++;
	}
	return (count);
}

static void	free_words(char **words, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		free(words[i]);
		i++;
	}
	free(words);
}

static int	get_word_len(const char *s, char c)
{
	char	*next;

	next = ft_strchr(s, c);
	if (next)
		return (next - s);
	return (ft_strlen(s));
}

static int	fill_words(char **words, const char *s, char c)
{
	int	i;
	int	word_index;
	int	word_len;

	i = 0;
	word_index = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (!s[i])
			break ;
		word_len = get_word_len(s + i, c);
		words[word_index] = malloc(word_len + 1);
		if (!words[word_index])
			return (word_index);
		ft_strlcpy(words[word_index], s + i, word_len + 1);
		i += word_len;
		word_index++;
	}
	return (-1);
}

/// @brief Divide the str in sub strs using c as separator.
/// @param s
/// @param c
/// @return words
char	**ft_split(char const *s, char c)
{
	char	**words;
	int		word_count;
	int		res;

	if (!s)
		return (NULL);
	word_count = count_words(s, c);
	words = malloc(sizeof(char *) * (word_count + 1));
	if (!words)
		return (NULL);
	res = fill_words(words, s, c);
	if (res != -1)
	{
		free_words(words, res);
		return (NULL);
	}
	words[word_count] = NULL;
	return (words);
}
