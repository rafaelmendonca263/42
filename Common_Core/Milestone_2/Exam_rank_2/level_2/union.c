
#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int already_printed(char *s, int pos, char c)
{
    int i = 0;

    while (i < pos)
    {
        if (s[i] == c)
            return 1;
        i++;
    }
    return 0;
}

int main(int argc, char *argv[])
{
    int i;

    if (argc != 3)
    {
        ft_putchar('\n');
        return 0;
    }

    i = 0;
    while (argv[1][i])
    {
        if (!already_printed(argv[1], i, argv[1][i]))
            ft_putchar(argv[1][i]);
        i++;
    }

    i = 0;
    while (argv[2][i])
    {
        if (!already_printed(argv[2], i, argv[2][i]) &&
            !already_printed(argv[1], -1, argv[2][i]))
            ft_putchar(argv[2][i]);
        i++;
    }

    ft_putchar('\n');
    return (0);
}
