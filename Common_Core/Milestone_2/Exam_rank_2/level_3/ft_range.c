
#include <stdlib.h>

int	*ft_range(int start, int end)
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
	while (i < size)
	{
        range[i] = start;
        if (start < end)
            start++;
        else
            start--;
        i++;
	}
	return (range);
}

#include <stdio.h>
#include <stdlib.h>

int *ft_range(int start, int end);

int main(void)
{
    int *arr;
    int i;
    int size;

    arr = ft_range(0, -3);
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
