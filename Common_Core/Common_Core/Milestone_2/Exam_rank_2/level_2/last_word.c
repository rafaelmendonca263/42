
#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int main(int argc, char *argv[])
{
    int i;

    if (argc != 2)
    {
        ft_putchar('\n');
        return (0);
    }

    i = 0;
    while (argv[1][i])
        i++;
    i--;

    while (i >= 0 && ((argv[1][i] >= 9 && argv[1][i] <= 12) || argv[1][i] == 32))
        i--;

    if (i < 0)
    {
        ft_putchar('\n');
        return (0);
    }

    while (i >= 0 && !((argv[1][i] >= 9 && argv[1][i] <= 12) || argv[1][i] == 32))
        i--;
    i++;

    while (argv[1][i] && !((argv[1][i] >= 9 && argv[1][i] <= 12) || argv[1][i] == 32))
    {
        ft_putchar(argv[1][i]);
        i++;
    }
    ft_putchar('\n');
    return (0);
}

