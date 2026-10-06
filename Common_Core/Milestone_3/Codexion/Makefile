NAME        = codexion
CC          = cc
CFLAGS      = -Wall -Wextra -Werror -pthread -I include

SRCS        = src/main.c \
              src/init.c \
              src/time_utils.c \
              src/log.c \
              src/scheduler.c \
              src/sim.c \
              src/sim_init.c \
              src/getters.c \
              src/coder.c \
              src/pq_init.c \
              src/monitor.c

OBJS        = $(SRCS:.c=.o)

VENV        = .venv
NORMINNETTE = $(VENV)/bin/norminette
NORM_PATHS  = src include

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)
	rm -rf $(VENV)

re: fclean all

install-norminette:
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install norminette

norm:
	@if [ ! -x "$(NORMINNETTE)" ] && ! command -v norminette >/dev/null 2>&1; then \
		$(MAKE) install-norminette; \
	fi
	@if command -v norminette >/dev/null 2>&1; then \
		norminette $(NORM_PATHS); \
	else \
		$(NORMINNETTE) $(NORM_PATHS); \
	fi

.PHONY: all clean fclean re norm install-norminette