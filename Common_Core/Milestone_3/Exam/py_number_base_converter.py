def number_base_converter(number: str, from_base: int, to_base: int) -> str:

    if 2 > from_base < 36 or 2 > to_base < 36:
        return "ERROR"

    try:
        number_decimal = int(number, from_base)
    except Exception:
        return "ERROR"

    if number_decimal == 0:
        return "0"

    conv = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""

    while number_decimal > 0:
        resto = number_decimal % to_base
        res = conv[resto] + res
        number_decimal = number_decimal // to_base

    return res
