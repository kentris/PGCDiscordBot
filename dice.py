from collections import namedtuple
import random
import re


DiceRoll = namedtuple("DiceRoll", "number_of_dice number_of_sides")


def process(message):
    message = process_dice_message(message)
    dice_rolls = process_dice_rolls(message)
    rolls = []
    for dr in dice_rolls:
        roll = roll_dice(dr.number_of_dice, dr.number_of_sides)
        rolls.append(roll)
    return rolls


def process_dice_message(message):
    """
    Assumed command format is: !roll <dice_format>
    We therefore strip the beginning command, and process the remainder.
    """
    # Consider a few different common formats for how users might make the call
    dice = message.replace('!roll: ', '')
    dice = dice.replace('!roll ', '')
    dice = dice.replace('!roll', '')
    return dice


def process_dice_rolls(message):
    """
    The user may roll a combination of dice rolls
    :param message:
    :return:
    """
    # Only want strings that fit the pattern 2d5
    die_pattern = "^\d+[dD]-?\d+$"
    rolls = message.split(" ")
    filtered_rolls = []
    for roll in rolls:
        if re.match(die_pattern, roll):
            if 'd' in roll:
                n_dice, n_sides = roll.split('d')
            elif 'D' in roll:
                n_dice, n_sizes = roll.split('D')
            n_dice, n_sides = int(n_dice), int(n_sides)
            filtered_rolls.append(DiceRoll(n_dice, n_sides))

    return filtered_rolls


def roll_dice(number_of_dice, number_of_sides):
    """
    Roll dice according to the specifications.
    :param number_of_dice: The number of dice to roll
    :param number_of_sides:  The number of sides on the dice
    :return:
    """
    roll = []
    for i in range(number_of_dice):
        if number_of_sides < 1:
            result = random.randint(number_of_sides, 0)
        else:
            result = random.randint(1, number_of_sides)
        roll.append(result)
    return roll
