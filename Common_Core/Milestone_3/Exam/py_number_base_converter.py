def number_base_converter(number: str,
                          from_base: int,
                          to_base: int) -> str:

    if from_base <= 1 or from_base >= 37:
        return "ERROR"
    if to_base <= 1 or to_base >= 37:
        return "ERROR"

    digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    try:
        num_decimal = int(number, from_base)
    except Exception:
        return "ERROR"

    if num_decimal == 0:
        return "0"

    resultado_base = ""
    while num_decimal > 0:
        res = num_decimal % to_base
        resultado_base = digitos[res] + resultado_base
        num_decimal = num_decimal // to_base

    return resultado_base


print(number_base_converter("1010", 2, 10))
print(number_base_converter("FF", 16, 10))
print(number_base_converter("255", 10, 16))
print(number_base_converter("123", 10, 2))
print(number_base_converter("Z", 36, 10))
print(number_base_converter("35", 10, 36))
print(number_base_converter("123", 1, 10))
print(number_base_converter("G", 16, 10))
