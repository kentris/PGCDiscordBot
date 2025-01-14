from discord.ext import commands
import discord
import json
import time
import dice
import joke
import blackjack
import money


# Open Discord password file and relevant channel information
with open('password.json', 'r') as file:
    data = json.load(file)
TOKEN = data['DISCORD_TOKEN']
GUILD = data['DISCORD_GUILD']
CHANNEL = data['CHANNEL_ID']

# Create the bot and set up the command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# The bot connects to the discord channel
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='helpme')
async def helpme(message):
    available_commands = ["help", "joke", "roll"]


@bot.command(name='beg')
async def beg(message):
    amount = money.beg(str(message.author.id))
    if amount == 0:
        await message.channel.send('"OUT OF MY WAY, PEASANT!"')
        await message.channel.send(f"You've earned no chips...")
    elif amount < 4:
        await message.channel.send('*throws a smattering of coins at you*')
        await message.channel.send(f"You've earned {amount} chips.")
    elif amount < 7:
        await message.channel.send(f'"Keep a stiff upper lip, eh?"')
        await message.channel.send(f"You've earned {amount} chips.")
    elif amount < 10:
        await message.channel.send(f'"Of course, of course, here you are, sir."')
        await message.channel.send(f"You've earned {amount} chips!")
    else:
        await message.channel.send(f"*presses a large coin into your palm*")
        await message.channel.send(f"You've earned a whole {amount} chips!")


@bot.command(name='balance')
async def get_balance(message):
    funds = money.get_balance(str(message.author.id))
    await message.channel.send(f"You have {funds} chips available")


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
    author_id = str(message.author.id)
    def check(msg):
        return msg.author == message.author and msg.content.lower() in ['hit', 'stand', 'doubledown']

    def check_money(msg):
        funds = money.get_balance(str(msg.author.id))
        return msg.author == message.author and msg.content.isdigit() and 0 <= int(msg.content) <= funds

    # We're only interested in processing commands on a specific channel
    if message.channel.id in CHANNEL:
        # Start new game of blackjack
        game = blackjack.Blackjack()
        game.start_game()
        await message.send(f"Welcome to Blackjack!")
        await message.send("How much would you like to wager?")
        try:
            msg = await bot.wait_for('message', check=check_money, timeout=60)
        except:
            await message.send("Time is money pal, game over!")
            return

        bet = int(msg.content)

        while game.is_player_turn:
            # Print the game state, take player input
            await message.send(str(game))
            await message.send("Do you want to `hit`, `doubledown`, or `stand`?")
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

            elif msg.content.lower() == "doubledown":
                game.hit(game.player)
                game.is_player_turn = False

        # Keep hitting dealer until ending is achieved
        while not game.is_game_over():
            await message.send(str(game))
            game.hit(game.dealer)

        # Announce the results
        await message.send(str(game))
        if game.player.is_bust():
            money.lose_money(author_id, bet)
            await message.send("You bust, sorry!")
        elif game.dealer.is_bust():
            money.win_money(author_id, bet)
            await message.send("Dealer busts, you win!")
        elif game.player.total > game.dealer.total:
            money.win_money(author_id, bet)
            await message.send("You win!")
        elif game.player.total < game.dealer.total:
            money.lose_money(author_id, bet)
            await message.send("You lose, sorry!")
        else:
            await message.send("Push!")

        await get_balance(message)


bot.run(TOKEN)
