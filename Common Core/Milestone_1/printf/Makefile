# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/14 15:28:55 by rmedonca          #+#    #+#              #
#    Updated: 2025/11/07 23:21:10 by rmedonca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CC      = cc
CFLAGS  = -Wall -Wextra -Werror
NAME    = libftprintf.a

SRCS    = ft_atoi.c \
          ft_bzero.c \
          ft_calloc.c \
          ft_isalnum.c \
          ft_isalpha.c \
          ft_isascii.c \
          ft_isdigit.c \
          ft_isprint.c \
          ft_itoa.c \
          ft_lstadd_back.c \
          ft_lstadd_front.c \
          ft_lstclear.c \
          ft_lstdelone.c \
          ft_lstiter.c \
          ft_lstlast.c \
          ft_lstmap.c \
          ft_lstnew.c \
          ft_lstsize.c \
          ft_memchr.c \
          ft_memcmp.c \
          ft_memcpy.c \
          ft_memmove.c \
          ft_memset.c \
          ft_printf.c \
          ft_putchar_fd.c \
          ft_putendl_fd.c \
          ft_putnbr_base_fd.c \
          ft_putnbr_fd.c \
          ft_putstr_fd.c \
          ft_split.c \
          ft_strchr.c \
          ft_strdup.c \
          ft_striteri.c \
          ft_strjoin.c \
          ft_strlcat.c \
          ft_strlcpy.c \
          ft_strlen.c \
          ft_strmapi.c \
          ft_strncmp.c \
          ft_strnstr.c \
          ft_strrchr.c \
          ft_strtrim.c \
          ft_substr.c \
          ft_tolower.c \
          ft_toupper.c \

OBJS    = $(SRCS:.c=.o)

TEST    = ft_printf.c
TEST_OUT = a.out

all: $(NAME)

$(NAME): $(OBJS)
	@ar rcs $(NAME) $(OBJS)

%.o: %.c
	@$(CC)  -c $< -o $@

test: $(NAME) $(TEST)
	@$(CC)  $(TEST) -L. -lftprintf -o $(TEST_OUT)

clean:
	@rm -f $(OBJS)

fclean: clean
	@rm -f $(NAME) $(TEST_OUT)

re: fclean all

r: fclean all
	@make test
	@make clean

.PHONY: all clean fclean re test
