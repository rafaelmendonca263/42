
#include <stdlib.h>

int	*ft_rrange(int start, int end)
{
	int	i;
	int	size;
	int	*range;

	i = 0;
	if (end >= start)
	{
		size = end - start + 1;
	}
	else
		size = start - end + 1;
	range = malloc(sizeof(int) * size);
	if (!range)
		return (NULL);
	while (size >= 0)
	{
		range[i] = end;
		if (end < start)
			end++;
		else
			end--;
		i++;
		size--;
	}
	return (range);
}

#include <stdio.h>
#include <stdlib.h>

int	*ft_rrange(int start, int end);

int	main(void)
{
	int	*arr;
	int	i;
	int	size;

	arr = ft_rrange(0, -3);
	if (!arr)
		return (1);
	size = 4;
	i = 0;
	while (i < size)
	{
		printf("%d ", arr[i]);
		i++;
	}
	printf("\n");
	free(arr);
	return (0);
}
