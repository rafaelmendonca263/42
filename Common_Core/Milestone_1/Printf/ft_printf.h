/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 15:22:04 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/19 22:21:48 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <stddef.h>
# include <stdlib.h>
# include <unistd.h>

// Utilities
int		ft_printf(const char *format, ...);

// Display
int		ft_putchar_fd(char c, int fd);
void	ft_putendl_fd(char *s, int fd);
void	ft_putnbr_fd(int n, int fd);
int		ft_putnbr_base_fd(unsigned long long nbr, char *base, int fd);
int		ft_putstr_fd_printf(char *s, int fd);
void	ft_putstr_fd(char *s, int fd);

// Strings
size_t	ft_strlen(const char *s);

#endif