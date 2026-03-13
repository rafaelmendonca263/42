
def ft_count_harvest_recursive():
    days_until_harvest = int(input("Days until harvest: "))

    def helper(i):
        if i > days_until_harvest:
            print("Harvest time!")
            return
        print("Day", i)
        helper(i + 1)
    helper(1)
