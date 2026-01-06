
#include <string.h>

char	*ft_strpbrk(const char *s1, const char *s2)
{
    int i;
    int p;
    char *re = (char *)s1;

    i = 0;
    while(s1[i])
    {
        p = 0;
        while(s2[p])
        {
            if(s1[i] == s2[p])
                return (re);
            p++;
        }
        i++;
        re++;
    }
    return(NULL);
}
#include <stdio.h>
#include <string.h>

int main(void)
{
    const char *s = "hello, world";
    const char *accept = "e";

    char *p = strpbrk(s, accept);

    if (p)
        printf("Primeiro caracter encontrado: '%c'\n", *p);
    else
        printf("Nenhum caracter encontrado\n");

    return 0;
}