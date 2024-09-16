def translate_coffee(option):

    if option == '1':
        return "ESPRESSO"
    elif option == '2':
        return "LATTE"
    elif option == '3':
        return "CAPPUCCINO"
    else:
        return option.upper()

def format_value(input_value):
    return "{:.2f}".format(input_value)

def print_and_pause(message):
    print(message)
    input("\nPress enter to continue...")

def insert_coins(coin_type, value):

    spaces = 21
    formatted_text = f"$ How many {coin_type}? "
    left_padding_text = formatted_text.ljust(spaces)
    num_coins = input(f"{left_padding_text}")

    try:
        float_value = float(num_coins) * value
    except ValueError:
        float_value = -1

    if float_value < 0:
        float_value = 0
        print(f"Invalid! considering zero for {coin_type}")

    return float_value
