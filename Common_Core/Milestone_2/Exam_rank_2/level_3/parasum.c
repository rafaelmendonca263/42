
#include <unistd.h>

void ft_putchar(char c)
{
    write(1,&c,1);
}

void ft_putnbr(int nbr)
{
    if(nbr >= 10)
        ft_putnbr(nbr / 10);
    ft_putchar(nbr % 10 + '0');
}

int main(int argc, char *argv[])
{
    int i;

    i = 1;
    if(argc < 2)
    {
        ft_putchar('0');
        ft_putchar('\n');
        return(0);
    }
    while(argv[i])
        i++;
    ft_putnbr(i - 1);
    ft_putchar('\n');
    return(0);
}
