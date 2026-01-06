
char    *ft_strrev(char *str)
{
    int i;
    int p;
    char *copy;

    i = 0;
    while(str[i])
        i++;
    copy = malloc(sizeof(char) * i + 1);
    if(!copy)
        return(NULL);
    i = 0;
    while(str[i])
        copy[i] = str[i];
    copy[i] = '\0';
    i--;
    p = 0;
    while(i >= 0)
    {
        str[p] = copy[i];
        i--;
        p++;
    }
    free(copy);
    return (str);
}
