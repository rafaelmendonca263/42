
#include <unistd.h>

void ft_putchar(char c)
{
    write(1,&c,1);
}

int ft_atoi(char str[])
{
	int	res;
	int	sign;
	int	i;

	res = 0;
	sign = 1;
	i = 0;
    while(str[i] == ' ')
        i++;
    if(str[i] == '+' || str[i] == '-')
    {
        if(str[i] == '-')
			sign = -1;
	}
	while (str[i] && str[i] >= '0' && str[i] <= '9')
	{
		res = res * 10 + (str[i] - '0');
		i++;
	}
	return (res * sign);
}

void ft_putnbr(int nbr)
{
    if(nbr >= 10)
        ft_putnbr(nbr / 10);
    ft_putchar(nbr % 10 +'0');
    return;
}

void ft_putstr(char src[])
{
    int i;

    i = 0;
    while(src[i])
    {
        ft_putchar(src[i]);
        i++;
    }
    return;
}

int main(int argc, char *argv[])
{
    int i;
    int res;
    char *str1;
    char *str2;

    i = 0;
    if(argc != 2)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[1][i])
    {
        if(argv[1][i] < '0' || argv[1][i] > '9')
        {
            ft_putchar('\n');
            return(0);
        }
        i++;
    }
    i = 1;
    while(i <= 9)
    {
        str1 = " x ";
        str2 = " = ";

        res = ft_atoi(argv[1]);
        ft_putnbr(i);
        ft_putstr(str1);
        ft_putstr(argv[1]);
        ft_putstr(str2);
        ft_putnbr(res * i);
        ft_putchar('\n');
        i++;
    }
    return(0);
}