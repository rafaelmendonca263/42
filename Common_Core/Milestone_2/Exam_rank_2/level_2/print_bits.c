
#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

void	print_bits(unsigned char octet)
{
    int i;

    i = 128;
    while(i > 0)
    {
        if(i & octet)
            ft_putchar('1');
        else
            ft_putchar('0');
        i /= 2;
    }
    return;
}

int main(void)
{
	print_bits(8);
	ft_putchar('\n');
	return (0);
}
