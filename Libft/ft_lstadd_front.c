void ft_lstadd_front(t_list **lst, t_list *new)
{
    new_node->next = *lst;
    *lst = new;
}
