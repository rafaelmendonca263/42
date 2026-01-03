# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/16 00:27:45 by rmedonca          #+#    #+#              #
#    Updated: 2025/12/16 00:34:04 by rmedonca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CC      = cc
CFLAGS  = -Wall -Wextra -Werror
NAME    = push_swap.a

SRCS    = push_swap.c \

OBJS    = $(SRCS:.c=.o)

TEST    = push_swap.c
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