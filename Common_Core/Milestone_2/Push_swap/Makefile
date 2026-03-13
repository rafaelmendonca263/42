# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/16 00:27:45 by rmedonca          #+#    #+#              #
#    Updated: 2026/03/13 16:33:42 by rmedonca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CC      = cc
CFLAGS  = -Wall -Wextra -Werror
NAME    = push_swap

SRC_DIRS = . Operators Printf Libft
SRCS = src/check_arguments.c \
       src/ps_lstadd_back.c \
       src/ps_lstadd_front.c \
       push_swap.c \
       src/push_top.c \
       src/pop_top.c \
       src/order_3.c \
       src/order_5.c \
       src/chunks.c \
       src/push_back_to_a.c \
       src/push_to_b.c \
       src/is_sorted.c \
       src/clean_and_exit.c \
       src/build_stack_a.c \
       src/order_less_than_five.c \
       src/sort_all.c  \
       src/Operators/push_a.c \
       src/Operators/push_b.c \
       src/Operators/reverse_rotate_a.c \
       src/Operators/reverse_rotate_a_b.c \
       src/Operators/reverse_rotate_b.c \
       src/Operators/rotate_a.c \
       src/Operators/rotate_a_b.c \
       src/Operators/rotate_b.c \
       src/Operators/swap_a.c \
       src/Operators/swap_a_b.c \
       src/Operators/swap_b.c \
       Printf/ft_printf.c \
       Printf/ft_strlen.c \
       Printf/ft_putstr_fd_printf.c \
       Printf/ft_putnbr_fd.c \
       Printf/ft_putendl_fd.c \
       Printf/ft_putchar_fd.c \
       Printf/ft_putnbr_base_fd.c \
       Libft/ft_isdigit.c \
       Libft/ft_strncmp.c \
       Libft/ft_split.c \
       Libft/ft_strchr.c \
       Libft/ft_strlcpy.c \
       Libft/ft_strdup.c \
       Libft/ft_atol.c \

OBJS = $(SRCS:.c=.o)

INCLUDES = -I. -I./Printf -I./Libft

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

r: all clean
	clear
.PHONY: all clean fclean re r
