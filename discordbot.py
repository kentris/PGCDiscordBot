from discord.ext import commands
import discord
import json
import time
import dice
import joke
import blackjack
import money
import huh


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


@bot.command(name='huh')
async def huh(message):
    info = huh.process_huh_message(message)
    for i in info:
        await message.channel.send(i)


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
    await get_balance(message)


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

    def can_double_down(msg, bet, game):
        num_cards = len(game.player.cards)
        funds = money.get_balance(str(msg.author.id))
        return 2*bet <= funds and num_cards == 2

    def can_split(message, bet, game):
        # TODO: Need to handle multiple hands
        return False

    # We're only interested in processing commands on a specific channel
    if message.channel.id in CHANNEL:
        # Start new game of blackjack
        game = blackjack.Blackjack()
        game.start_game()

        funds = money.get_balance(str(message.author.id))
        await message.send(f"Welcome to Blackjack!")
        await message.send(f"You have {funds} chips available. How much would you like to wager?")
        try:
            msg = await bot.wait_for('message', check=check_money, timeout=60)
        except:
            await message.send("Time is money pal, game over!")
            return

        bet = int(msg.content)

        while game.is_player_turn:
            # Print the game state, take player input
            await message.send(str(game))
            if can_double_down(message, bet, game) and can_split(message, bet, game):
                await message.send("Do you want to `hit`, `doubledown`, `split`, or `stand`?")
            elif can_double_down(message, bet, game):
                await message.send("Do you want to `hit`, `doubledown`, or `stand`?")
            elif can_split(message, bet, game):
                await message.send("Do you want to `hit`, `split`, or `stand`?")
            else:
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
            # Player doubles down
            elif msg.content.lower() == "doubledown" and can_double_down(message, bet, game):
                bet *= 2
                game.hit(game.player)
                game.is_player_turn = False
            # Player tries to doubledown but can't afford it
            elif msg.content.lower() == "doubledown" and not can_double_down(message, bet, game):
                if len(game.player.cards) > 2:
                    await message.send("You're wasting everybody's time. You already took a card!")
                else:
                    await message.send("You're wasting everybody's time. You don't have the coin!")
            # Player inputs something we can't handle
            else:
                await message.send("You're wasting everybody's time.")

        await message.send(str(game))
        await message.send("----------------")
        # Keep hitting dealer until ending is achieved
        while not game.is_game_over():
            await message.send("Dealer takes a card:")
            game.hit(game.dealer)
            await message.send(str(game))
            await message.send("----------------")


        # Announce the results
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
