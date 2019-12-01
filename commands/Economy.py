from discord.ext import commands
from discord import Embed
from discord import Colour
import discord
from economy.Money_type import MoneyType
from commands.Coin_converter import CoinType
from commands.Amount_converter import Amount
from economy.Economy import amountToString
import random
import typing
import config

def can_modify_economy():
    async def predicate(ctx):
        return ctx.guild.get_role(config.can_modify_economy).position <= ctx.author.top_role.position
    return commands.check(predicate)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Usage = "The roll commands"

    @commands.command(name="wallet", aliases=["w"])
    async def wallet(self, ctx, user: typing.Optional[discord.Member]):
        if user == None:
            user = ctx.author
        embed = Embed(colour=Colour.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="RS3 Balance", value=amountToString(self.bot.get_amount(user.id, MoneyType.RS3)), inline=False)
        embed.add_field(name="07 Balance", value=amountToString(self.bot.get_amount(user.id, MoneyType.R07)), inline=False)
        await ctx.send(embed=embed)

    @can_modify_economy()
    @commands.command(name="set")
    async def set_wallet(self, ctx, type: CoinType, user: discord.Member, amount: Amount):
        embed = Embed(colour=Colour.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Set Request", value=f"Successfully set {type.formatString()} to {amountToString(amount)} for {user.mention} wallet", inline=False)
        await ctx.send(embed=embed)
        self.bot.set_amount(user.id, amount, type)

    @can_modify_economy()
    @commands.command(name="update")
    async def update(self, ctx, type: CoinType, user: discord.Member, amount: Amount):
        embed = Embed(colour=Colour.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Update Request", value=f"Successfully updated {amountToString(amount)} {type.formatString()} to {user.mention} wallet", inline=False)
        await ctx.send(embed=embed)
        self.bot.update_amount(user.id, amount, type)


    @wallet.error
    async def wallet_info_error(self, ctx, error):
        await self.info_error(ctx, error, "![w | wallet] user")


    @set_wallet.error
    async def wallet_info_error(self, ctx, error):
        await self.info_error(ctx, error, "!set [rs3 | 07] user amount")


    @update.error
    async def wallet_info_error(self, ctx, error):
        await self.info_error(ctx, error, "!update [rs3 | 07] user amount")


    async def info_error(self, ctx, error, usage):
        embed = Embed(colour=Colour.red())
        embed.set_footer(text=usage)
        embed.add_field(name='Error', value=error.args[0].replace("Command raised an exception: Exception: ", ""))
        await ctx.send(embed=embed)