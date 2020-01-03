import random

from discord import Colour
from discord import Embed
from discord import Message
from discord import TextChannel
from discord import Guild
from discord.ext import commands

from commands.Amount_converter import Amount
from commands.Coin_converter import CoinType
from economy.Economy import amountValid
from economy.Economy import amountToString
from enum import Enum

import time

data = {}
cards_names = [
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 2
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 3
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 4
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 4
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 5
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 6
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 7
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 8
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 9
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    },
    {
        "emoji": "<:BetaGate2_Key1_Clue_HyKwIEkVVxk4:662527301669486617>",
        "value": 10
    }
]


class Winner(Enum):
    AUTHOR = 0
    BOT = 1
    TIE = 2


def calculate_total(cards):
    total = 0
    for card in cards:
        total += card["value"]
    return total


async def embed_cards(deck):
    cards = "".join(map(lambda card: card["emoji"], deck))
    total = " + ".join(map(lambda card: str(card["value"]), deck)) + f" = {calculate_total(deck)}"
    return f"{cards}\n{total}"


async def print_embed(id):
    embed = Embed()

    player_deck = data[id]["author_cards"]
    embed.add_field(name="Player", value=await embed_cards(player_deck))

    bot_deck = data[id]["bot_cards"]
    embed.add_field(name="Bot", value=await embed_cards(bot_deck))

    if data[id]["msg_id"] is None:
        data[id]["msg_id"] = await data[id]["channel"].send(embed=embed)
    else:
        await data[id]["msg_id"].edit(embed=embed)


def get_winner_at_moment(id):
    author_total = calculate_total(data[id]["author_cards"])
    bot_total = calculate_total(data[id]["bot_cards"])

    if bot_total > 21 and author_total > 21:
        return Winner.TIE

    if author_total > 21:
        return Winner.BOT

    if bot_total > 21:
        return Winner.AUTHOR

    if bot_total == author_total:
        return Winner.TIE

    return Winner.BOT if bot_total > author_total else Winner.AUTHOR


async def bust(id):

    embed = Embed(colour=Colour.red(), description="Bust I win! Better luck next time.")

    player_deck = data[id]["author_cards"]
    embed.add_field(name="Player", value=await embed_cards(player_deck))

    bot_deck = data[id]["bot_cards"]
    embed.add_field(name="Bot", value=await embed_cards(bot_deck))

    if data[id]["msg_id"] is None:
        data[id]["msg_id"] = await data[id]["channel"].send(embed=embed)
    else:
        await data[id]["msg_id"].edit(embed=embed)


    data.pop(id)


async def hit(id):
    data[id]["author_cards"].append(draw_card(id))
    if calculate_total(data[id]["author_cards"]) > 21:
        await bust(id)
    else:
        await print_embed(id)


def draw_card(id):
    return data[id]["deck"].pop()


def finish(id, bot_win: Winner):

    if bot_win == Winner.AUTHOR:
        bot_win = Winner()
        # todo stuff


class BlackJack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.Usage = "The blackjack commands"

    @commands.command(name="bj")
    async def bj_command(self, ctx, coin_type: CoinType, amount: Amount):
        amountValid(self.bot, ctx.author.id, amount, coin_type)
        author_id = ctx.author.id

        if author_id in data:
            raise Exception("You are already in a blackjack game, please use hit or stand")

        data[author_id] = {
            "channel": ctx.channel,
            "msg_id": None,
            "bot_cards": [],
            "deck": cards_names * 4,
            "author_stand": False,
            "bot_stand": False,
            "type": coin_type,
            "amount": amount,
            "ended": False
        }
        random.shuffle(data[author_id]["deck"])
        data[author_id]["author_cards"] = [draw_card(author_id), draw_card(author_id)]

        self.bot.update_amount(author_id, -amount, coin_type)
        await print_embed(author_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("hit"):
            if message.author.id in data:
                await message.delete()
                await hit(message.author.id)
                return
            embed = Embed(colour=Colour.red())
            embed.set_footer(text="Usage: !bj type amount")
            embed.add_field(name='Error', value="You are not in a game!")
            await message.channel.send(embed=embed)

        if message.content.lower().startswith("stand"):
            if message.author.id in data:
                await message.delete()
                return
            embed = Embed(colour=Colour.red())
            embed.set_footer(text="Usage: !bj type amount")
            embed.add_field(name='Error', value="You are not in a game!")
            await message.send(embed=embed)

    @bj_command.error
    async def info_error(self, ctx, error):
        embed = Embed(colour=Colour.red())
        embed.set_footer(text="Usage: !bj type amount")
        embed.add_field(name='Error', value=error.args[0].replace("Command raised an exception: Exception: ", ""))
        await ctx.send(embed=embed)
        raise error
