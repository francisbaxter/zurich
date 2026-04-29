import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import csv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Defines intents without using .all()
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Loads list of quotes
with open('./zurich_quotes.csv', newline='') as f:
    reader = csv.reader(f)
    zurich_quotes = list(reader)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    # Checks if author of message is the bot itself, and ignores if it is
    if message.author == bot.user:
        return

    # Checks if sent message is a command, if so passes to commands processer and returns
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return

    # If message is not a command or from bot, percentage chance to send quote
    percentage_chance = 0.015 # 1.5%
    if random.random() < percentage_chance:
        response = random.choice(zurich_quotes)[0]
        await message.channel.send(response)


# Retrieve a random quote manually
@bot.command(name='zurich')
async def zurich(ctx):
    response = random.choice(zurich_quotes)[0]
    await ctx.send(response)


bot.run(TOKEN)
