
#include <unistd.h>

void ft_putchar(char c)
{
    write(1,&c,1);
}

int main(int argc, char *argv[])
{
    int i;
    int p;
    int j;
    int check;

    i = 0;
    if (argc != 3)
    {
        ft_putchar('\n');
        return(0);
    }
    while(argv[1][i])
    {
        j = i - 1;
        
        while(j >= 0)
        {
            if(argv[1][i] == argv[1][j])
            {
                check = 0;
                break;
            }
            j--;
        }
        p = 0;
        while(argv[2][p] && check == 1)
        {
            if(argv[1][i] == argv[2][p])
            {
                ft_putchar(argv[1][i]);
                break;
            }
            p++;
        }
        i++;
    }
    ft_putchar('\n');
    return(0);
}
