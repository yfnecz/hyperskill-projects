def price_string(func):
    def wrapper(arg):
        return "£" + str(func(arg))

    return wrapper


@price_string
def new_price(price):
    return round(price * 0.9, 1)


print(new_price(100))