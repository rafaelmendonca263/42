def fizz_buzz_list(n: int) -> list[str]:
    res = []
    i = 1

    while (i <= n):
        stri = ""

        if (i % 3 == 0):
            stri += 'Fizz'
            
        if (i % 5 == 0):
            stri += 'Buzz'
        
        if stri == "":
            res.append(str(i))
        else:
            res.append(stri)

        i = i + 1

    return res

print(fizz_buzz_list(15))
#['1', '2', 'Fizz', '4', 'Buzz',
# 'Fizz', '7', '8', 'Fizz', 'Buzz', '11',
# 'Fizz', '13', '14', 'FizzBuzz']