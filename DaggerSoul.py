# DaggerSoul.py

import discord
from discord.ext import commands
import random
import re
import os
import webserver

TOKEN = os.environ['discordkey'] # hides the Diskord token as an environment key

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='soul')
async def soul(ctx, dice_input: str):
    if dice_input.lower() == 'help':
	    await soul_help(ctx)
    elif dice_input.lower() == 'adv':
	    await roll_duality_dice(ctx, advantage=True)
    elif dice_input.lower() == 'dis':
        await roll_duality_dice(ctx, disadvantage=True)
    elif dice_input.lower() == 'duality':
        await roll_duality_dice(ctx)
    else:
        match = re.match(r'(\d*)d(\d+)(\+(\d+))?', dice_input)
        if match:
            await roll_dice(ctx, match)
        else:
	        ctx.send(f"Invalid dice format. Please write in 'mdn+x' format (for example: '2d6' or '2d6+3'). If you are trying to roll Duality Dice use the command `!soul duality`.")

async def roll_duality_dice(ctx, advantage=False, disadvantage=False):
    hope_roll = random.randint(1, 12)
    fear_roll = random.randint(1, 12)

    await ctx.send(f"Rolling the Duality Dice...")
    await ctx.send(f"Hope Die: {hope_roll}")
    await ctx.send(f"Fear Die: {fear_roll}")

    if hope_roll != fear_roll:
        sum_roll = hope_roll + fear_roll
        if advantage:
            extra_d6 = random.randint(1, 6)
            await ctx.send(f"Advantage: Rolling extra d6 = {extra_d6}")
            sum_roll += extra_d6
        elif disadvantage:
            extra_d6 = random.randint(1, 6)
            await ctx.send(f"Disadvantage: Rolling extra d6 = {extra_d6}")
            sum_roll -= extra_d6

        if hope_roll > fear_roll:
            result = f"Result = {sum_roll} with HOPE! Add a Hope Token to Character Sheet!"
            
        else:
            result = f"Result = {sum_roll} with FEAR! Add a Fear Token to Action Tracker! (Action Tracker Coming Soon)"
            
    else:
        result = f"It's a Critical Success! Increment Stress and Hope by 1!!"
        
    
    await ctx.send(result)

async def roll_dice(ctx, match):
    num_rolls = int(match.group(1)) if match.group(1) else 1
    dice_size = int(match.group(2))
    modifier = int(match.group(4)) if match.group(4) else 0

    total_roll = 0
    rolls = []
    for _ in range(num_rolls):
        roll = random.randint(1, dice_size)
        rolls.append(roll)
        total_roll += roll

    total_roll += modifier

    await ctx.send(f"Rolling {num_rolls}d{dice_size}{f'+{modifier}' if modifier else ''}: {rolls}")
    await ctx.send(f"Total: {total_roll}")

async def soul_help(ctx):
    embed = discord.Embed(
        title="DaggerSoul Bot Commands",
        description="Here are the commands you can use with the DaggerSoul Bot:",
        color=0x2F3136  # Dark gray for the embed box
    )

    embed.add_field(
        name="`!soul <dice>`",
        value="Rolls dice of a specified size (e.g., `!soul 2d6+3`).",
        inline=False
    )
    embed.add_field(
        name="`!soul duality`",
        value="Rolls the Duality Dice (Hope and Fear).",
        inline=False
    )
    embed.add_field(
        name="`!soul adv`",
        value="Rolls the Duality Dice with advantage (extra d6 added).",
        inline=False
    )
    embed.add_field(
        name="`!soul dis`",
        value="Rolls the Duality Dice with disadvantage (extra d6 subtracted).",
        inline=False
    )
    embed.add_field(
        name="`!soul help`",
        value="Displays this help message.",
        inline=False
    )

    embed.set_footer(text="Use the correct format to roll dice (e.g., '2d6+3').")
    
    await ctx.send(embed=embed)


webserver.keep_alive()
bot.run(TOKEN) # key must not be stored in the code, rather in the webserver as an environment key
