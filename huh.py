import re

def process(message):
    message = process_huh_message(message)
    if len(message) == 0:
        info = huh_info()
    elif message == 'beg':
        info = beg_info()
    elif message == 'balance':
        info = balance_info()
    elif message == 'blackjack':
        info = blackjack_info()
    elif message == 'joke':
        info = joke_info()
    elif message == 'roll':
        info = roll_info()
    else:
        info = huh_info()
        info.insert(0, "None of the specified commands were recognized.")

    return info


def process_huh_message(message):
    """
    Assumed command format is: `!huh <command>` or `!huh`
    We therefore strip the beginning command, and process the remainder.
    """
    # Consider a few different common formats for how users might make the call
    huh_message = message.replace('!huh: ', '')
    huh_message = huh_message.replace('!huh ', '')
    huh_message = huh_message.replace('!huh', '')
    return huh_message.lower().strip()

def huh_info():
    available_commands = [
        "huh",
        "beg",
        "balance",
        "blackjack",
        "joke",
        "roll"
    ]
    msg = [
        "BobDoleBob supports the following commands:",
        ', '.join(['`!'+cmd+'`' for cmd in available_commands]),
        'For more information on a command, please type:',
        '*!huh <command>*'
    ]

    return msg

def beg_info():
    msg = [
        "`!beg` allows the user to debase themselves for a few measly chips.",
        "These chips can be used in games supported by BobDoleBot, such as BlackJack."
    ]
    return msg

def balance_info():
    msg = [
        '`!balance` informs the user of the current total chips in their possession.'
    ]
    return msg

def blackjack_info():
    msg = [
        '`!blackjack` allows the user to play a game of BlackJack where they can wager up to however many chips they have in their possession.',
        'For more rules regarding BlackJack, [please visit the BlackJack wiki page](https://en.wikipedia.org/wiki/Blackjack).'
    ]
    return msg

def joke_info():
    msg = [
        '`!joke` provides the user with a joke of questionable quality.'
    ]
    return msg

def roll_info():
    msg = [
        '`!roll` allows the user to simulate a dice roll of many combinations.',
        'This command requires the user to specify the number of dice and how many sides a die has.',
        'The format to specify the number of dice and how many sides a dice has is *<number_of_dice>d<number_of_sides>*.'
        'For example, to roll 2 6-sided dice, the user would type in `!roll 2d6`.'
    ]
    return msg
