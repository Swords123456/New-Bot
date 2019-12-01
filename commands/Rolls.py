from discord.ext import commands
from discord import Embed
from discord import Colour
from economy.Money_type import MoneyType
from commands.Coin_converter import CoinType
from commands.Amount_converter import Amount
from economy.Economy import amountToString
import random

async def roll(bot, ctx, amount, type, chance, multiplier):
    rolled = random.randint(0, 100)
    if bot.get_amount(ctx.author.id, type) < amount:
        raise Exception(f"Not enough {type.formatString()}")

    hasWon = rolled > chance;

    if hasWon:
        embed = Embed(colour=Colour.green())
    else:
        embed = Embed(colour=Colour.red())

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Dice game", 
        value=f"Rolled {rolled} out of 100. You {'won' if hasWon else 'lost'} {amountToString((amount * multiplier) - amount) if hasWon else amountToString(amount)} {type.formatString()}"
        )

    await ctx.send(embed=embed)
    if hasWon:
        bot.update_amount(ctx.author.id, (amount * multiplier) - amount, type)
    else:
        bot.update_amount(ctx.author.id, -amount, type)

class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Usage = "The roll commands"

    @commands.command(name="50")
    async def roll_50(self, ctx, type: CoinType, amount: Amount):
        await roll(self.bot, ctx, amount, type, 50, 1.75)

    @commands.command(name="54")
    async def roll_54(self, ctx, type: CoinType, amount: Amount):
        await roll(self.bot, ctx, amount, type, 54, 2)

    @commands.command(name="75")
    async def roll_75(self, ctx, type: CoinType, amount: Amount):
        await roll(self.bot, ctx, amount, type, 75, 3)

    @commands.command(name="95")
    async def roll_75(self, ctx, type: CoinType, amount: Amount):
        await roll(self.bot, ctx, amount, type, 95, 5)

    @roll_50.error
    @roll_54.error
    @roll_75.error
    async def info_error(self, ctx, error):
        embed = Embed(colour=Colour.red())
        embed.set_footer(text="Usage: ![50 | 54 | 75] [rs3 | 07] amount")
        embed.add_field(name='Error', value=error.args[0].replace("Command raised an exception: Exception: ", ""))
        await ctx.send(embed=embed)