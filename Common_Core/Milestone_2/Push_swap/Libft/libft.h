/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 15:22:04 by rmedonca          #+#    #+#             */
/*   Updated: 2026/01/22 00:10:34 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LIBFT_H
# define LIBFT_H

# include <stddef.h>
# include <stdio.h>
# include <stdlib.h>
# include <unistd.h>

// Utilities
int		ft_isdigit(int c);

// Strings
size_t	ft_strlen(const char *s);
int		ft_strncmp(const char *s1, const char *s2, const unsigned int n);
char	**ft_split(char const *s, char c);
size_t	ft_strlcpy(char *dst, const char *src, size_t size);
char	*ft_strchr(const char *s, int c);
long	ft_atol(const char *str);

// Memory
char	*ft_strdup(const char *s);

#endif