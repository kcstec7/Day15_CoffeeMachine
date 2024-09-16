# Day 15: Coffee machine
# Find emoji: https://emojipedia.org/hot-beverage
# Add emojis: https://support.microsoft.com/en-gb/windows/windows-keyboard-tips-and-tricks-588e0b72-0fff-6d3f-aeee-6e5116097942
# PyCharm keyboard shortcuts: https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html?keymap=secondary_windows

import os
import time
from Day_15_Menu import menu
from Day_15_GenericFunctions import translate_coffee
from Day_15_GenericFunctions import format_value
from Day_15_GenericFunctions import print_and_pause
from Day_15_GenericFunctions import insert_coins

dict_resources = {
    'water_ml': {
        'type': 'Water',
        'amount': 300,
        'prefix': '',
        'measure': 'ml',
    },
    'milk_ml': {
        'type': 'Milk',
        'amount': 200,
        'prefix': '',
        'measure': 'ml',
    },
    'coffee_g': {
        'type': 'Coffee',
        'amount': 100,
        'prefix': '',
        'measure': 'g',
    },
    'cash': {
        'type': 'Money',
        'amount': 2.50,
        'prefix': '$',
        'measure': '',
        'coins_type': {
            'quarters': 0.25,
            'dimes': 0.10,
            'nickles': 0.05,
            'pennies': 0.01,
        },
        'coins_value': {
            'quarters': 1.00,
            'dimes': 1.00,
            'nickles': 0.45,
            'pennies': 0.05,
        }
    }
}

def check_resources(drink, available_resources):

    drink_recipe = menu[drink]['recipe']
    message = ""

    for key in drink_recipe:
        if drink_recipe[key] > available_resources[key]['amount']:
            message = f"\nSorry, there is not enough {available_resources[key]['type'].lower()}\n"

    if message == "":
        return True
    else:
        print_and_pause(message)
        return False

def get_resources_report():

    textToReturn = "\n"

    for resource_key in dict_resources:

        dots = 13 - len(str(dict_resources[resource_key]['type']))

        if resource_key == "cash":

            print_amount = str(format_value(dict_resources[resource_key]['amount']))
            measure_text = dict_resources[resource_key]['prefix'] + print_amount
            right_padding_text = format(measure_text.rjust(dots, '.'))
            textToReturn += f"{dict_resources[resource_key]['type']}{right_padding_text}\n"

            for coin, value_coin in dict_resources[resource_key]['coins_value'].items():

                spaces = 13 - len(str(coin))
                formatted_value = f"${format_value(value_coin)}"
                left_padding_coin = format(formatted_value.rjust(spaces, ' '))
                textToReturn += f"      + {coin.title()}: {left_padding_coin}\n"

        else:
            print_amount = str(dict_resources[resource_key]['amount'])
            measure_text = dict_resources[resource_key]['prefix'] + print_amount + dict_resources[resource_key]['measure']
            right_padding_text = format(measure_text.rjust(dots, '.'))
            textToReturn += f"{dict_resources[resource_key]['type']}{right_padding_text}\n"

    return textToReturn

def process_coins(change, value_received_per_coin):

    global dict_resources

    if change == 0:  # Means the value paid was exact

        for coin, value in value_received_per_coin.items():
            if value > 0:
                dict_resources['cash']['coins_value'][coin] += value

        return True

    elif change < 0:  # Means the value paid is smaller than the price

        print_and_pause(f"\nSorry that's not enough money. Money refunded.")
        return False

    elif change > 0:  # Means there has to be some value returned to the customer

        print(f"Change: US${format_value(change)}")

        change_to_return = change
        dict_final_available_value = {}

        for coin, value in dict_resources['cash']['coins_value'].items():

            coin_value_changed = False

            value_available_per_coin = value
            single_coin_value = dict_resources['cash']['coins_type'][coin]

            if value_received_per_coin[coin] > 0:
                coin_value_changed = True
                value_available_per_coin += value_received_per_coin[coin]

            while change_to_return >= single_coin_value and value_available_per_coin > 0:
                coin_value_changed = True
                change_to_return -= single_coin_value
                value_available_per_coin -= single_coin_value

            if coin_value_changed:
                dict_final_available_value[coin] = value_available_per_coin

        if change_to_return != 0:

            # Does not update the amount of cash per coin
            print_and_pause("There was an issue when trying to return the change. Please try again.")
            return False

        else:

            # Updates the amount of cash per coin
            for coin, value in dict_final_available_value.items():
                dict_resources['cash']['coins_value'][coin] = value

            return True

def receive_payment(price):

    value_received = 0
    value_received_per_coin = {
        'quarters': 0,
        'dimes': 0,
        'nickles': 0,
        'pennies': 0,
    }

    print(f"That's US${format_value(price)}. Please insert coins.")

    for key, value in dict_resources['cash']['coins_type'].items():

        float_value = insert_coins(key, value)

        value_received += float_value
        value_received_per_coin[key] += float_value

        if value_received >= price:
            break

    change = value_received - price

    print("-" * 24)
    print(f"Value received: US${format_value(value_received)}")
    if value_received == 0:
        print_and_pause(f"\nSorry, can't proceed without payment.")
        return False

    if process_coins(change, value_received_per_coin):
        dict_resources['cash']['amount'] += price
        print_and_pause("Processed coins!")
        return True
    # The message is given before:
    # else:
    #     print_and_pause("Did not process coins!")
    #     return False

def prepare_coffee(drink):

    os.system("cls")
    dots = "."
    print(f"Preparing coffee...")
    for number in range(1, 6):
        print(f"{dots}")
        dots += "."
        time.sleep(1)

    drink_recipe = menu[drink]['recipe']

    for ingredient in drink_recipe:
        dict_resources[ingredient]['amount'] = dict_resources[ingredient]['amount'] - drink_recipe[ingredient]

    print_and_pause(f"\nHere's your {drink.title()}. Enjoy!\n")

def session():
    """This is the function for when the machine is ON"""
    os.system("cls")

    global dict_resources

    menu_option = ""
    coffee_options = ["ESPRESSO", "LATTE", "CAPPUCCINO"]

    while menu_option == "":

        menu_option = translate_coffee(input("\nWhat would you like? ([1] Espresso/ [2] Latte / [3] Cappuccino): "))

        if any(element in menu_option for element in coffee_options):

            if not check_resources(menu_option, dict_resources):
                break

            if not receive_payment(menu[menu_option]['price_dollar']):
                break

            prepare_coffee(menu_option)

        elif menu_option == "REPORT":
            report = get_resources_report()
            print_and_pause(report)
        elif menu_option == "OFF":
            return False
        else:
            menu_option = ""
            print("That's not a valid option. Please try again.")

    return True

machine_on = True
while machine_on:
    machine_on = session()

print("The machine is being turned OFF.")
