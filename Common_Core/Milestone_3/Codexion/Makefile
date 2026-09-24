NAME = codexion
CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread -I include
SRCS = src/main.c src/init.c src/time_utils.c src/log.c src/scheduler.c src/sim.c src/sim_init.c src/getters.c src/coder.c src/pq_init.c src/monitor.c
TEST_PQ = src/test_pq.c
VENV = .venv
NORMINNETTE = $(VENV)/bin/norminette
NORM_PATHS = src include

.DEFAULT_GOAL := all

all: $(NAME) clean

$(NAME): install $(SRCS)
	@$(CC) $(CFLAGS) -o $(NAME) $(SRCS)

install:
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install norminette

clean:
	@rm -f *.o

fclean: clean
	@rm -f $(NAME)
	@rm -rf $(VENV)

re: fclean all

norm: all
	@if [ ! -x "$(NORMINNETTE)" ]; then $(MAKE) install-norminette; fi
	@$(NORMINNETTE) $(NORM_PATHS)

.PHONY: all clean fclean re test test-pq codexion_asan asan-run norm install-norminette