from discord.ext import commands
from commands.DD import DD


class Games(commands.Cog):
    def __init__(self, bot):
        DD(bot, self)