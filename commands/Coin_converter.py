from discord.ext import commands
from economy.Money_type import Money_type

class CoinType(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.lower() == "rs3":
            return Money_type.RS3;
        elif argument.lower() == "07":
            return Money_type.R_07
        elif argument.lower() == "token":
            return Money_type.TOKENS
        else:
            raise commands.BadArgument(f"{argument} is not a rs3, 07 or tokens")