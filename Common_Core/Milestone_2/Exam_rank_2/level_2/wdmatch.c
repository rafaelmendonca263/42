
#include <unistd.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int main(int argc, char *argv[])
{
    int i;
    int p;
    int check;
    
    i = 0;
    p = 0;
    if(argc != 3)
    {
        ft_putchar('\n');
        return(0);
    }
        while (argv[1][i] && argv[2][p])
    {
        if (argv[1][i] == argv[2][p])
            i++;
        p++;      
    }
    if(argv[1][i] == '\0')
    {
        i = 0;
        while (argv[1][i])
        {   
            ft_putchar(argv[1][i]);
            i++;
        }
    }
    ft_putchar('\n');
    return(0);
}
