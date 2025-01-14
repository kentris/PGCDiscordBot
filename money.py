import json
import os
import random


dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "money.json")

def read_money():
    """Reads data from a JSON file and returns it as a Python dictionary."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        return None

def write_money(data):
    """Writes data to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully written to '{file_path}'")
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")

def beg(user):
    amount = random.randint(0, 10)
    funds = read_money()
    if user not in funds:
        funds[user] = amount
    else:
        funds[user] += amount
    write_money(funds)
    return amount

def get_balance(user):
    funds = read_money()
    return funds.get(user, 0)