
#include "stdio.h"
#include "stdlib.h"

int	main(int argc, char *argv[])
{
	int	i;
	int	num;

	i = 2;
	if (argc == 2)
	{
		num = atoi(argv[1]);
		if (num == 1)
			printf("1");
		while (i <= num)
		{
			if (num % i == 0)
			{
				printf("%d", i);
				if (num != i)
					printf("*");
				num = num / i;
			}
			else
				i++;
		}
	}
	printf("\n");
	return (0);
}
