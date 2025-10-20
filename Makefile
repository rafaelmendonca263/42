# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmedonca <rmedonca@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/14 15:28:55 by rmedonca          #+#    #+#              #
#    Updated: 2025/10/16 15:27:19 by rmedonca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Variáveis
CC = cc
CFLAGS = -Wall -Wextra -Werror
NAME = libft.a
SRCS = 	ft_atoi.c		ft_bzero.c
		ft_calloc.c		ft_isalnum.c
		ft_isalpha.c	ft_isascii.c
		ft_isdigit.c	ft_isprint.c
		ft_memchr.c		ft_memchr.c
		ft_memcmp.c		ft_memcpy.c
		ft_memmove.c	ft_memset.c
		ft_strchr.c		ft_strdup.c
		ft_strlcat.c	ft_strlcpy.c
		ft_strlen.c		ft_strncmp.c
		ft_strnstr.c	ft_strrchr.c
		ft_tolower.c	ft_toupper.c
OBJS = $(SRCS:.c=.o)

# Target padrão
all: $(NAME)

# Regra para criar a biblioteca
$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

# Regra genérica para compilar .c → .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Apagar ficheiros objeto
clean:
	-rm -f $(OBJS)

# Apagar .o + biblioteca
fclean: clean
	-rm -f $(NAME)

# Recompilar tudo
re: fclean
	make all

