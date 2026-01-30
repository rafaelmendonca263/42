# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/14 15:28:55 by rmedonca          #+#    #+#              #
#    Updated: 2025/11/19 22:23:59 by rmedonca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CC      = cc
CFLAGS  = -Wall -Wextra -Werror
NAME    = libftprintf.a

SRCS    = ft_printf.c \
          ft_putchar_fd.c \
          ft_putendl_fd.c \
          ft_putnbr_base_fd.c \
          ft_putstr_fd_printf.c \
          ft_strchr.c \
          ft_strlen.c \

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
