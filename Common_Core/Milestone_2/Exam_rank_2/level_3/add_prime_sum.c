
#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_putnbr(int nbr)
{
	unsigned int	nb;

	if (nbr < 0)
	{
		ft_putchar('-');
		nb = -nbr;
	}
	else
		nb = nbr;
	if (nb >= 10)
		ft_putnbr(nb / 10);
	ft_putchar(nb % 10 + '0');
}

int	ft_atoi(char *str)
{
	int	res;
	int	sign;
	int	i;

	res = 0;
	sign = 1;
	i = 0;
	while (str[i] == ' ')
		i++;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			sign = -1;
	}
	while (str[i] && str[i] >= 48 && str[i] <= 57)
	{
		res = res * 10;
		res = str[i] - 48;
		i++;
	}
	return (res * sign);
}
int	is_prime(int nbr)
{
	int	i;

	if (nbr < 2)
		return (0);
	i = 2;
	while (i <= nbr / 2)
	{
		if (nbr % i == 0)
			return (0);
		i++;
	}
	return (1);
}

int	main(int argc, char *argv[])
{
	int	i;
	int	sum;
	int	n;

	i = 0;
	if (argc != 2 || ft_atoi(argv[1] <= 0))
	{
		write(1, "\n", 1);
		return (0);
	}
	n = ft_atoi(argv[1]);
	sum = 0;
	while (n > 1)
	{
		if (is_prime(n))
			sum += n;
		n--;
	}
	ft_putnbr(sum);
	ft_putchar('\n');
}
