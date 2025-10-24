/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: psilva-p <psilva-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/08/09 17:35:26 by psilva-p          #+#    #+#             */
/*   Updated: 2025/08/09 20:00:44 by psilva-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

extern int	g_clues[16];

void	ft_error(void);
void	ft_putchar(char c);
int		occ_num(char *str);



int main (int argc, char **argv)
{
	int index;

	index = 0;
	if (argc != 2)
	{
		ft_error;
		return ;
	}
	else
	{
		if (occ_num(argv[1] == -1))
			ft_error();
		else
		{
			ft_error;
			return ;
		}


	}

}
