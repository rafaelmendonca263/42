/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 18:59:47 by rmedonca          #+#    #+#             */
/*   Updated: 2025/10/24 17:31:13 by rmedonca         ###   ########.fr       */
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

static int	free_words(char **words, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		free(words[i]);
		i++;
	}
	free(words);
	return (1);
}

static int	fill_words(char **words, const char *s, char c, int word_count)
{
	int		i;
	int		word_index;
	char	*next;
	int		word_len;

	i = 0;
	word_index = 0;
	while (word_index < word_count)
	{
		while (s[i] && s[i] == c)
			i++;
		next = ft_strchr(s + i, c);
		if (next)
			word_len = next - (s + i);
		else
			word_len = ft_strlen(s + i);
		words[word_index] = malloc(word_len + 1);
		if (!words[word_index])
			return (1);
		ft_strlcpy(words[word_index], s + i, word_len + 1);
		i += word_len;
		word_index++;
	}
	return (0);
}

char	**ft_split(char const *s, char c)
{
	char	**words;
	int		word_count;

	if (!s)
		return (NULL);
	word_count = count_words(s, c);
	words = malloc(sizeof(char *) * (word_count + 1));
	if (!words)
		return (NULL);
	if (fill_words(words, s, c, word_count))
	{
		free_words(words, word_count);
		return (NULL);
	}
	words[word_count] = NULL;
	return (words);
}

/* int	main(void)
{
	char	**res;
	int		i;

	res = ft_split("  hello  world 42  ", ' ');
	i = 0;
	while (res[i])
	{
		printf("'%s'\n", res[i]);
		free(res[i]);
		i++;
	}
	free(res);
} */
