
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    int res;
    int i;
    int numb1;
    int numb2;

    i = 1;
    if(argc != 3)
    {
        printf("\n");
        return(0);
    }
    numb1 = atoi(argv[1]);
    numb2 = atoi(argv[2]);
    if (numb1 > 0 && numb2 > 0)
    {
        if(numb1 == numb2)
        {
            res = numb1;
        }
        else if(numb1 > numb2)
        {
            while(i <= numb1)
            {
                if((numb1 % i == 0) && (numb2 % i == 0))
                {
                    res = i;
                }
                i++;
            }
        }
        else
        {
            while(i <= numb2)
            {
                if((numb1 % i == 0) && (numb2 % i == 0))
                {
                    res = i;
                }
                i++;
            }
        }
    }
    printf("%d\n",res);
    return(0);
}
