import discord
import json
import os
import pickle
from textdistance import jaro_winkler
import time
import dice
import lol
import joke

# Open Discord password file and relevant channel information
with open('password.json', 'r') as file:
    data = json.load(file)
TOKEN = data['DISCORD_TOKEN']
GUILD = data['DISCORD_GUILD']
CHANNEL = data['CHANNEL_ID']

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
    if message.channel.id in CHANNEL:
        # Process the `lol!` command
        if '!lol' in message.content:
            # If there is any issue, msg2 will be blank
            msg1, msg2 = lol.process(message)
            await message.channel.send(msg1)
            await message.channel.send(msg2)
        elif '!joke' in message.content:
            msg1, msg2 = joke.process(message)
            # print out joke
            await message.channel.send(msg1)
            if msg2:
                time.sleep(2)
                await message.channel.send(msg2)
        elif '!roll' in message.content:
            rolls = dice.process(message)
            for roll in rolls:
                total = sum(roll)
                await message.channel.send(roll)
                await message.channel.send(total)


client.run(TOKEN)
