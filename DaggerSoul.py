#DaggerSoul.py

import discord
from discord.ext import commands
import random
import re
import os
import webserver

TOKEN = os.environ['discordkey'] # hides the Discord token as an environment key

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Daggerheart | !soul help"))

@bot.command(name='soul')
async def soul(ctx, dice_input: str = None, *args):
    if not dice_input:
        await soul_help(ctx)
        return
        
    if dice_input.lower() == 'help':
        await soul_help(ctx)
    elif dice_input.lower() == 'adv':
        await roll_duality_dice(ctx, advantage=True)
    elif dice_input.lower() == 'dis':
        await roll_duality_dice(ctx, disadvantage=True)
    elif dice_input.lower() == 'duality':
        await roll_duality_dice(ctx)
    elif dice_input.lower() == 'online':
        await ctx.send("ok")
    else:
        # Check for advantage or disadvantage in args
        advantage = 'adv' in [arg.lower() for arg in args]
        disadvantage = 'dis' in [arg.lower() for arg in args]
        
        match = re.match(r'(\d*)d(\d+)(\+(\d+))?', dice_input)
        if match:
            await roll_dice(ctx, match, advantage, disadvantage)
        else:
            await ctx.send(f"Invalid dice format. Please write in 'mdn+x' format (for example: '2d6' or '2d6+3'). If you are trying to roll Duality Dice use the command `!soul duality`.")

async def roll_duality_dice(ctx, advantage=False, disadvantage=False):
    hope_roll = random.randint(1, 12)
    fear_roll = random.randint(1, 12)
    extra_d6 = None
    sum_roll = hope_roll + fear_roll
    
    # Create an embed for a nicer message
    if hope_roll > fear_roll:
        color = 0xFFD700  # Yellow/Gold for Hope
        result_type = "Hope"
        result_message = "Add a Hope Token to Character Sheet!"
        emoji = "✨"
    elif fear_roll > hope_roll:
        color = 0x9932CC  # Dark Purple for Fear
        result_type = "Fear"
        result_message = "Add a Fear Token!"
        emoji = "💀"
    else:
        color = 0xFFD700  # Gold for Critical Success
        result_type = "Critical Success"
        result_message = "Increment Stress and Hope by 1!!"
        emoji = "🌟"
    
    embed = discord.Embed(
        title=f"[ {sum_roll} with {result_type} {emoji} ]",
        description=result_message,
        color=color
    )
    
    # Add dice information
    dice_info = [
        ("**Dice to Roll**", ""),
        ("Hope", f"(d12) → {hope_roll}"),
        ("Fear", f"(d12) → {fear_roll}")
    ]
    
    if advantage:
        extra_d6 = random.randint(1, 6)
        sum_roll += extra_d6
        dice_info.append(("Advantage", f"(d6) → +{extra_d6}"))
        embed.title = f"[ {sum_roll} with {result_type} {emoji} ]"
    elif disadvantage:
        extra_d6 = random.randint(1, 6)
        sum_roll -= extra_d6
        dice_info.append(("Disadvantage", f"(d6) → -{extra_d6}"))
        embed.title = f"[ {sum_roll} with {result_type} {emoji} ]"
    
    embed.add_field(name=f"{emoji} **Rolled with {result_type}**", value="", inline=False)
    
    # Add base information
    embed.add_field(name="Base", value="(d12)", inline=False)
    
    # Add dice roll section
    rolls_text = "\n".join([f"{name}: {value}" for name, value in dice_info if name and value])
    if rolls_text:
        embed.add_field(name="Dice Rolls", value=rolls_text, inline=False)
    
    # Add result section
    result_text = f"Hope: {hope_roll}(d12), Fear: {fear_roll}, Mod: +0\n= {sum_roll}"
    embed.add_field(name="Result", value=result_text, inline=False)
    
    # Add timestamp (matches the competitor's format)
    embed.set_footer(text=ctx.message.created_at.strftime("%d/%m/%Y %H:%M"))
    
    await ctx.send(embed=embed)

async def roll_dice(ctx, match, advantage=False, disadvantage=False):
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
    
    # Add advantage/disadvantage 
    extra_d6 = None
    if advantage:
        extra_d6 = random.randint(1, 6)
        total_roll += extra_d6
    elif disadvantage:
        extra_d6 = random.randint(1, 6)
        total_roll -= extra_d6
    
    # Create an embed for a nicer message
    embed = discord.Embed(
        title=f"Rolling {num_rolls}d{dice_size}{f'+{modifier}' if modifier else ''}",
        description=f"**Result: {total_roll}**",
        color=0x7289DA  # Discord blurple color
    )
    
    embed.add_field(name="Dice Rolls", value=str(rolls), inline=False)
    
    # Build calculation text
    calculation_parts = []
    calculation_parts.append(f"{sum(rolls)} (dice)")
    
    if modifier:
        calculation_parts.append(f"{modifier} (modifier)")
    
    if extra_d6:
        if advantage:
            calculation_parts.append(f"{extra_d6} (advantage d6)")
        elif disadvantage:
            calculation_parts.append(f"-{extra_d6} (disadvantage d6)")
    
    calculation = " + ".join(calculation_parts)
    if disadvantage and extra_d6:
        calculation = calculation.replace(f"-{extra_d6}", f"- {extra_d6}")
    
    calculation += f" = {total_roll}"
    
    embed.add_field(name="Calculation", value=calculation, inline=False)
    
    embed.set_footer(text=ctx.message.created_at.strftime("%d/%m/%Y %H:%M"))
    
    await ctx.send(embed=embed)

async def soul_help(ctx):
    embed = discord.Embed(
        title="DaggerSoul Bot Commands",
        description="Here are the commands you can use with the DaggerSoul Bot:",
        color=0x00FFFF  # Blue for Help
    )

    embed.add_field(
        name="`!soul <dice>`",
        value="Rolls dice of a specified size (e.g., `!soul 2d6+3`).",
        inline=False
    )
    embed.add_field(
        name="`!soul <dice> adv`",
        value="Rolls dice with advantage (adds a d6).",
        inline=False
    )
    embed.add_field(
        name="`!soul <dice> dis`",
        value="Rolls dice with disadvantage (subtracts a d6).",
        inline=False
    )
    embed.add_field(
        name="`!soul duality`",
        value="Rolls the Duality Dice (Hope and Fear).",
        inline=False
    )
    embed.add_field(
        name="`!soul duality adv` or `!soul adv`",
        value="Rolls the Duality Dice with advantage (extra d6 added).",
        inline=False
    )
    embed.add_field(
        name="`!soul duality dis` or `!soul dis`",
        value="Rolls the Duality Dice with disadvantage (extra d6 subtracted).",
        inline=False
    )
    embed.add_field(
        name="`!soul help` or `!soul`",
        value="Displays this help message.",
        inline=False
    )

    embed.set_footer(text="Use the correct format to roll dice (e.g., '2d6+3').")

    await ctx.send(embed=embed)

webserver.keep_alive()
bot.run(TOKEN) # key must not be stored in the code, rather in the webserver as an environment key
