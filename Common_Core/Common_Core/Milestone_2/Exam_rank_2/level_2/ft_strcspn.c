
size_t	ft_strcspn(const char *s, const char *reject)
{
    int i;
    int p;

    i = 0;
    while(s[i])
    {
        p = 0;
        while(reject[p])
        {
            if(s[i] == reject[p])
                return(i);
            p++;
        }
        i++;
    }
    return(i);
}
