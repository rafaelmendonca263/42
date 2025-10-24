#include <unistd.h>
#include <stdio.h>

int	g_grid[4][4];
int	g_clues[16];

int	occ_num(char *str)
{
	int counter;

	counter = 0;
	while (*str)
	{
		if (*str >= '1' && *str <= '4')
		{
			counter++;
			str++;
			if (counter < 16)
			{
				if (*str != ' ')
					return (-1);
			}
			str++;
		}
		else
			return (-1);
	}
	return (counter);
}


void	ft_error(void)
{
	write(2, "Error\n", 6);
}


void	ft_putchar(char c)
{
	write(1, &c, 1);
}




/*
int main ()
{
	char str[] = "olas 12 tt 6 ii 4";
	printf("%i\n", occ_num(str));
}
*/
