def format_price(price):
    price = int(price)
    return "Цена: {} руб.".format(price)

result = format_price(56.24)
display_price = result
print(display_price)