from collections import Counter
import os
import pickle
import random


with open(os.path.join("data", "dadjokes.txt")) as file:
    dadjokes = file.readlines()


def process(message):
    """Handle processing the Discord messaging for joke prompts"""
    # Get a random joke from our list of dad jokes
    dadjoke_idx = random.randint(0, len(dadjokes)-1)
    dadjoke = dadjokes[dadjoke_idx]
    msg1, msg2 = process_dad_joke(dadjoke)
    return msg1, msg2


def process_dad_joke(dadjoke):
    msg1 = ""
    msg2 = ""
    if '? ' in dadjoke:
        msgs = dadjoke.split("? ", 1)
        msg1 = msgs[0] + '?'
        msg2 = msgs[1]
    elif '! ' in dadjoke:
        msgs = dadjoke.split("! ", 1)
        msg1 = msgs[0] + '!'
        msg2 = msgs[1]
    elif Counter(dadjoke)['.'] > 1:
        msgs = dadjoke.split(". ", 1)
        if len(msgs) > 1:
            msg1 = msgs[0] + '.'
            msg2 = msgs[1]
        else:
            msg1 = dadjoke
    else:
        msg1 = dadjoke

    return msg1, msg2
