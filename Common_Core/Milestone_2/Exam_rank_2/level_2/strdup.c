
char    *ft_strdup(char *src)
{
    char *tmp;
    int len;
    int i;

    while(src[len])
        len++;
    *tmp = malloc(sizeof(char) * len + 1)
    if(!tmp)
        return(NULL);
    while(src[i])
    {
        tmp[i] = src[i];
        i++;
    }
    tmp[i] = '\0';
    return(tmp); 
}
