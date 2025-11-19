/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rmedonca <rmedonca@student.42lisboa.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 22:07:53 by rmedonca          #+#    #+#             */
/*   Updated: 2025/11/19 22:28:31 by rmedonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	no_condition(const char *format, int i)
{
	ft_putchar_fd('%', 1);
	ft_putchar_fd(format[i + 1], 1);
	return (2);
}

static int	condition_p(va_list args)
{
	void	*ptr;
	int		count;

	ptr = va_arg(args, void *);
	if (!ptr)
		return (ft_putstr_fd_printf("(nil)", 1));
	count = 0;
	count += ft_putstr_fd_printf("0x", 1);
	count += ft_putnbr_base_fd((unsigned long long)ptr, "0123456789abcdef", 1);
	return (count);
}

static int	condition_d_i(va_list args)
{
	long	n;
	int		count;

	n = va_arg(args, int);
	count = 0;
	if (n < 0)
	{
		count += ft_putchar_fd('-', 1);
		n = -n;
	}
	count += ft_putnbr_base_fd((unsigned long long)n, "0123456789", 1);
	return (count);
}

static int	conditions(int i, va_list args, const char *format)
{
	int	count;

	count = 0;
	if (format[i + 1] == 'c')
		count += ft_putchar_fd(va_arg(args, int), 1);
	else if (format[i + 1] == 's')
		count += ft_putstr_fd_printf(va_arg(args, char *), 1);
	else if (format[i + 1] == 'p')
		count += condition_p(args);
	else if (format[i + 1] == 'd' || format[i + 1] == 'i')
		count += condition_d_i(args);
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
	else
		count += no_condition(format, i);
	return (count);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		i;
	int		count;

	if (!format)
		return (0);
	va_start(args, format);
	i = -1;
	count = 0;
	while (format[++i])
	{
		if (format[i] == '%')
		{
			if (!format[i + 1])
				return (va_end(args), -1);
			count += conditions(i, args, format);
			i++;
		}
		else
			count += ft_putchar_fd(format[i], 1);
	}
	va_end(args);
	return (count);
}

/* #include "libft.h"
#include <limits.h>
#include <stdint.h>
#include <stdio.h>void	ft_putstr_fd(char *s, int fd)

int	main(void)
{
	int ret1, ret2;
	ret1 = ft_printf("Pointer NULL: %p\n", (void *)NULL);
	ret2 = printf("Pointer NULL: %p\n", (void *)NULL);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Pointer zero: %p\n", (void *)0x0);
	ret2 = printf("Pointer zero: %p\n", (void *)0x0);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Pointer max: %p\n", (void *)UINT64_MAX);
	ret2 = printf("Pointer max: %p\n", (void *)UINT64_MAX);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Empty string: '%s'\n", "");
	ret2 = printf("Empty string: '%s'\n", "");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("NULL string: '%s'\n", (char *)NULL);
	ret2 = printf("NULL string: '%s'\n", (char *)NULL);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Special string: '%s'\n", "Line1\nLine2\tTab %");
	ret2 = printf("Special string: '%s'\n", "Line1\nLine2\tTab %");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Symbols string: %s\n", "(#!$%%&/=?»«*++^~n");
	ret2 = printf("Symbols string: %s\n", "(#!$%%&/=?»«*++^~n");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Zero int: %d\n", 0);
	ret2 = printf("Zero int: %d\n", 0);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("INT_MAX: %d\n", INT_MAX);
	ret2 = printf("INT_MAX: %d\n", INT_MAX);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("INT_MIN: %d\n", INT_MIN);
	ret2 = printf("INT_MIN: %d\n", INT_MIN);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Unsigned zero: %u\n", 0U);
	ret2 = printf("Unsigned zero: %u\n", 0U);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Unsigned max: %u\n", UINT_MAX);
	ret2 = printf("Unsigned max: %u\n", UINT_MAX);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Hex zero: %x\n", 0U);
	ret2 = printf("Hex zero: %x\n", 0U);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Hex max: %X\n", UINT_MAX);
	ret2 = printf("Hex max: %X\n", UINT_MAX);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Hex mix: %x %X\n", 305419896U, 305419896U);
	ret2 = printf("Hex mix: %x %X\n", 305419896U, 305419896U);
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Char normal: %c\n", 'A');
	ret2 = printf("Char normal: %c\n", 'A');
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Char newline: %c\n", '\n');
	ret2 = printf("Char newline: %c\n", '\n');
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Char null: %c\n", '\0');
	ret2 = printf("Char null: %c\n", '\0');
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Percent: %%\n");
	ret2 = printf("Percent: %%\n");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Multiple percent: %%%% %%\n");
	ret2 = printf("Multiple percent: %%%% %%\n");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Percent end: %%");
	ret2 = printf("Percent end: %%"); // evita warning
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	ret1 = ft_printf("Unknown specifier: %%q\n");
	ret2 = printf("Unknown specifier: %%q\n");
	printf("ret1 = %d | ret2 = %d\n\n", ret1, ret2);
	return (0);
} */
