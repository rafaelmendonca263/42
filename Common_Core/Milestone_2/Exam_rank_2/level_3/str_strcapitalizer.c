
#include <unistd.h>

void ft_putchar(char c)
{
    write(1,&c,1);
}

int is_space(char c)
{
    if(c <= 32)
        return(1);
    return(0);
}

int main(int argc, char *argv[])
{
    int i;
    int p;

    i = 1;
    if(argc < 2)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[i])
    {
        p = 0;
        while(argv[i][p])
        {
            if(argv[i][p] >= 'A' && argv[i][p] <= 'Z')
                argv[i][p] = argv[i][p] + 32;
            if((argv[i][p] >= 'a' && argv[i][p] <= 'z') && is_space(argv[i][p - 1]))
                argv[i][p] = argv[i][p] - 32;
            ft_putchar(argv[i][p]);
            p++;
        }
        ft_putchar('\n');
        i++;
    }
    return(0);
}
