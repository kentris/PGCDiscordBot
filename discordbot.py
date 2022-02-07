import discord
import json
import pickle
from textdistance import jaro_winkler

# Open Discord password file and relevant channel information
with open('password.json', 'r') as file:
    data = json.load(file)
TOKEN = data['DISCORD_TOKEN']
GUILD = data['DISCORD_GUILD']
CHANNEL = data['CHANNEL_ID']

# Read in preprocessed Champions list
with open('lolchampions.pkl', 'rb') as file:
    champions = pickle.load(file)
champion_names = list(champions.keys())


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


client = discord.Client()


# The bot connects to the discord channel
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


# The bot processes messages
@client.event
async def on_message(message):
    # Ignore any messages from the bot
    if message.author == client.user:
        return

    # We're only interested in processing commands on a specific channel
    if message.channel.id == CHANNEL:
        # Process the `lol!` command
        if '!lol' in message.content:
            # Get the user_input for the champ
            champ_input = process_lol_message(message.content)
            # Find the best match for the user input
            champ = match_lol_champ(champ_input)
            # Grab the corresponding champs' urls
            build_url = champions[champ]['build_url']
            info_url = champions[champ]['move_url']
            # Push to discord channel
            await message.channel.send(f"How to play {champ}: {info_url}")
            await message.channel.send(f"How to build {champ}: {build_url}")


client.run(TOKEN)
