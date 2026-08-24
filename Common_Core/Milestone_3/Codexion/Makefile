NAME = codexion
CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread -I include
SRCS = src/main.c src/init.c src/time_utils.c src/log.c src/scheduler.c src/sim.c src/coder.c src/monitor.c

TEST_PQ = src/test_pq.c

all: $(NAME)

$(NAME): $(SRCS)
	$(CC) $(CFLAGS) -o $(NAME) $(SRCS)

clean:
	rm -f *.o

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re

test: $(NAME)
	sh ./tests/run_tests.sh

test-pq:
	$(CC) $(CFLAGS) -o test_pq $(TEST_PQ) src/scheduler.c
	./test_pq

codexion_asan: $(SRCS)
	$(CC) -g -fsanitize=address -fno-omit-frame-pointer -I include -pthread -o $@ $(SRCS)

asan-run: codexion_asan
	./codexion_asan 3 200 50 50 50 1 10 fifo

norm:
	@command -v norminette >/dev/null 2>&1 && norminette . || { echo "norminette not found — install with: python3 -m pip install --user norminette"; exit 1; }

