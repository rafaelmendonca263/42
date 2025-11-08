/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 22:07:53 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/07 23:57:56 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	condition_p(va_list args)
{
	void	*ptr;
	int		count;

	ptr = va_arg(args, void *);
	if (!ptr)
		return (ft_putstr_fd("(nil)", 1));
	count = ft_putstr_fd("0x", 1);
	count += ft_putnbr_base_fd((unsigned long long)ptr, "0123456789abcdef", 1);
	return (count);
}

static int	conditions(int i, va_list args, const char *format)
{
	int	count;

	count = 0;
	if (format[i + 1] == 'c')
		count += ft_putchar_fd(va_arg(args, int), 1);
	else if (format[i + 1] == 's')
		count += ft_putstr_printf(va_arg(args, char *), 1);
	else if (format[i + 1] == 'p')
		count += condition_p(args);
	else if (format[i + 1] == 'd' || format[i + 1] == 'i')
		count += ft_putnbr_base_fd(va_arg(args, int), "0123456789", 1);
	else if (format[i + 1] == 'u')
		count += ft_putnbr_base_fd(va_arg(args, unsigned int), "0123456789", 1);
	else if (format[i + 1] == 'x')
		count += ft_putnbr_base_fd(va_arg(args, unsigned int),
				"0123456789abcdef", 1);
	else if (format[i + 1] == 'X')
		count += ft_putnbr_base_fd(va_arg(args, unsigned int),
				"0123456789ABCDEF", 1);
	else if (format[i + 1] == '%')
		count += ft_putchar_fd('%', 1);
	return (count);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		i;
	int		count;

	va_start(args, format);
	if (!format)
		return (0);
	i = 0;
	count = 0;
	while (format[i])
	{
		if (format[i] == '%')
			count += conditions(i++, args, format);
		else
		{
			ft_putchar_fd(format[i], 1);
			count++;
		}
		i++;
	}
	va_end(args);
	return (count);
}

 #include <stdio.h>

int	main(void)
{
	int	ret2;
	int	*nbr;

	// int	ret1;
	char ***************cleaned;
	nbr = &ret2;
			printf("   %p\n", cleaned);
	return (ft_printf("%p\n", cleaned));
}
	// printf("%p\n", NULL);/*
	// ret1 = ft_printf("Olá, mundo!\n");
	// ret2 = printf("Olá, mundo!\n");
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("Número: %d\n", 42);
	// ret2 = printf("Número: %d\n", 42);
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("Hexadecimal: %x\n", 255);
	// ret2 = printf("Hexadecimal: %x\n", 255);
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("Caractere: %c\n", 'A');
	// ret2 = printf("Caractere: %c\n", 'A');
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("String: %s\n", "teste");
	// ret2 = printf("String: %s\n", "teste");
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("Ponteiro: %p\n", (void *)0x1234abcd);
	// ret2 = printf("Ponteiro: %p\n", (void *)0x1234abcd);
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// ret1 = ft_printf("Percentagem: %%\n");
	// ret2 = printf("Percentagem: %%\n");
	// printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	// return (0);
// }