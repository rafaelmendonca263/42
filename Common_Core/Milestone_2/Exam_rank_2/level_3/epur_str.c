
#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

int	main(int argc, char *argv[])
{
	int	i;
    int space;

	i = 0;
    space = 0;
	if (argc != 2)
	{
		ft_putchar("\n");
		return (0);
	}
    while(argv[1][i])
    {
        if(argv[1][i] <= 32)
            space = 1;
        if(argv[1][i] > 32)
        {
            if(space == 0)
            {
                ft_putchar(' ');
            }
            space = 0;
            ft_putchar(argv[1][i]);
        }
        i++;
    }
    ft_putchar("\n");
    return(0);
}
