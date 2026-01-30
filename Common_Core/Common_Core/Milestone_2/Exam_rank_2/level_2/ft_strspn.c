
#include <string.h>

size_t	ft_strspn(const char *s, const char *accept)
{
    int i;
    int p;
    int check;

    i = 0;
    while(s[i])
    {
        p = 0;
        check = 0;
        while(accept[p])
        {
            if(s[i] == accept[p])
                check = 1;
            p++;
        }
        if(check = 0)
            return(i);
        i++;
    }
    return(i);
}
#include <stdio.h>

/*int	main(void)
{
	const char	*s = "123abc";
	const char	*accept = "0123456789";

	printf("%zu\n", ft_strspn(s, accept));
	return (0);
}*/
