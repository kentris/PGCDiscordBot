import os
import pickle
from textdistance import jaro_winkler

# Read in preprocessed Champions list
with open(os.path.join('data', 'lolchampions.pkl'), 'rb') as file:
    champions = pickle.load(file)
champion_names = list(champions.keys())


def process(message):
    """Handle processing the Discord messaging for LoL prompts"""
    # Get the user_input for the champ
    champ_input = process_lol_message(message.content)
    # Make sure there is a champ to process
    if len(champ_input) == 0:
        error_msg = "No champ name was provided..."
        return error_msg, ""
    else:
        # Find the best match for the user input
        champ = match_lol_champ(champ_input)
        # Grab the corresponding champs' urls
        build_url = champions[champ]['build_url']
        info_url = champions[champ]['move_url']
        # Push to discord channel
        how_to_play = f"How to play {champ}: {info_url}"
        how_to_build = f"How to build {champ}: {build_url}"
        return how_to_play, how_to_build


def process_lol_message(message):
    """
    Assumed command format is: !lol <champ_name>
    We therefore strip the beginning command, and process the remainder.
    """
    # Consider a few different common formats for how users might make the call
    champ = message.replace('!lol: ', '')
    champ = champ.replace('!lol ', '')
    champ = champ.replace('!lol', '')
    return champ


def match_lol_champ(user_input):
    """Match user input to best guessed Champion"""
    similarity = [jaro_winkler(champ, user_input) for
                  champ in champion_names]
    idx = similarity.index(max(similarity))
    return champion_names[idx]