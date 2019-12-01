from discord.ext import commands
from discord import Embed
from discord import Colour
from economy.Money_type import Money_type
from commands.Coin_converter import CoinType
from commands.Amount_converter import Amount
from economy.Economy import amountToString
import random

async def roll(ctx, amount, type, chance, multiplier):
    rolled = random.randint(0, 100)

    hasWon = rolled > chance

    if hasWon:
        embed = Embed(colour=Colour.green())
    else:
        embed = Embed(colour=Colour.red())

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Dice game", value=f"Rolled {rolled} out of 100. You {'won' if hasWon else 'lost'} {amountToString(amount * multiplier) if hasWon else amountToString(amount)} {type.name}")

    await ctx.send(embed=embed)

class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Usage = "The roll commands"

    @commands.command(name="50")
    async def roll_50(self, ctx, amount: Amount, type: CoinType):
        await roll(ctx, amount, type, 50, 1.5)

    @commands.command(name="54")
    async def roll_54(self, ctx, amount: Amount, type: CoinType):
        await roll(ctx, amount, type, 54, 1.2)

    @commands.command(name="75")
    async def roll_75(self, ctx, amount: Amount, type: CoinType):
        await roll(ctx, amount, type, 75, 1.9)

    @roll_50.error
    @roll_54.error
    @roll_75.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = Embed()
            embed.set_footer(text="Usage: [!50|!54|!75] [rs3|07] amount")
            embed.add_field(name='Error', value=error)
            await ctx.send(embed=embed)
        else:
            raise error