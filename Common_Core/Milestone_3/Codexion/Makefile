NAME = codexion
CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread -I include
SRCS = src/main.c src/init.c src/time_utils.c src/log.c src/scheduler.c src/sim.c src/coder.c src/monitor.c
TEST_PQ = src/test_pq.c
VENV = .venv
NORMINNETTE = $(VENV)/bin/norminette
NORM_PATHS = src include

.DEFAULT_GOAL := all

all: $(NAME)

$(NAME): $(SRCS)
	$(CC) $(CFLAGS) -o $(NAME) $(SRCS)

install-norminette:
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install norminette

clean:
	rm -f *.o

fclean: clean
	rm -f $(NAME)
	rm -rf $(VENV)

re: fclean all

.PHONY: all clean fclean re test test-pq codexion_asan asan-run norm install-norminette

test: $(NAME)
	sh ./tests/run_tests.sh

test-pq:
	$(CC) $(CFLAGS) -o test_pq $(TEST_PQ) src/scheduler.c
	./test_pq

codexion_asan: $(SRCS)
	$(CC) -g -fsanitize=address -fno-omit-frame-pointer -I include -pthread -o $@ $(SRCS)

asan-run: codexion_asan
	./codexion_asan 3 200 50 50 50 1 10 fifo

norm: all
	@if [ ! -x "$(NORMINNETTE)" ]; then $(MAKE) install-norminette; fi
	@$(NORMINNETTE) $(NORM_PATHS)
