from discord.ext import commands
import discord
import json
import time
import dice
import lol
import joke
import blackjack

# Open Discord password file and relevant channel information
with open('password.json', 'r') as file:
    data = json.load(file)
TOKEN = data['DISCORD_TOKEN']
GUILD = data['DISCORD_GUILD']
CHANNEL = data['CHANNEL_ID']

# client = discord.Client()
# Create the bot and set up the command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# The bot connects to the discord channel
# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# The bot processes messages
# @client.event
# async def on_message(message):
#     # Ignore any messages from the bot
#     if message.author == client.user:
#         return
#
#     # We're only interested in processing commands on a specific channel
#     if message.channel.id in CHANNEL:
#         # Process the `lol!` command
#         if '!lol' in message.content:
#             # If there is any issue, msg2 will be blank
#             msg1, msg2 = lol.process(message)
#             await message.channel.send(msg1)
#             await message.channel.send(msg2)
#         elif '!joke' in message.content:
#             msg1, msg2 = joke.process(message)
#             # print out joke
#             await message.channel.send(msg1)
#             if msg2:
#                 time.sleep(2)
#                 await message.channel.send(msg2)
#         elif '!roll' in message.content:
#             rolls = dice.process(message.content)
#             for roll in rolls:
#                 total = sum(roll)
#                 await message.channel.send(roll)
#                 await message.channel.send(total)


@bot.command(name='joke')
async def tell_joke(message):
    # We're only interested in processing commands on a specific channel
    if message.channel.id in CHANNEL:
        msg1, msg2 = joke.process(message)
        # print out joke
        await message.channel.send(msg1)
        if msg2:
            time.sleep(2)
            await message.channel.send(msg2)


@bot.command(name='roll')
async def roll_dice(message):
    # We're only interested in processing commands on a specific channel
    if message.channel.id in CHANNEL:
        rolls = dice.process(message.content)
        for roll in rolls:
            total = sum(roll)
            await message.channel.send(roll)
            await message.channel.send(total)


@bot.command(name='blackjack')
async def blackjackgame(message):
    def check(msg):
        return msg.author == message.author and msg.content.lower() in ['hit', 'stand']

    # We're only interested in processing commands on a specific channel
    if message.channel.id in CHANNEL:
        # Start new game of blackjack
        game = blackjack.Blackjack()
        game.start_game()
        await message.send(f"Welcome to Blackjack!")

        while game.is_player_turn:
            # Print the game state, take player input
            print(game)
            await message.send("Do you want to `hit` or `stand`?")
            try:
                msg = await bot.wait_for('message', check=check, timeout=60)
            except:
                await message.send("Time is money pal, game over!")
                break

            # Player takes a card
            if msg.content.lower() == "hit":
                game.hit(game.player)
                if game.player.is_bust():
                    game.is_player_turn = False

            # Player passes
            elif msg.content.lower() == "stand":
                game.is_player_turn = False

        # Keep hitting dealer until ending is achieved
        while not game.is_game_over():
            print(game)
            game.hit(game.dealer)

        # Announce the results
        print(game)
        if game.player.is_bust():
            await message.send("You bust, sorry!")
        elif game.dealer.is_bust():
            await message.send("Dealer busts, you win!")
        elif game.player.total > game.dealer:
            await message.send("You win!")
        elif game.player.total < game.dealer:
            await message.send("You lose, sorry!")
        else:
            await message.send("Push!")


# client.run(TOKEN)
bot.run(TOKEN)
