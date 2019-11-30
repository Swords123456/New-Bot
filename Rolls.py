from discord.ext import commands

class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="54", usage="Hi bob")
    async def roll_54(self, ctx, amount: int):
    	ctx.send("hey")

    @commands.command(name="75", usage="Hi bob")
    async def roll_75(self, ctx, amount: int):
    	ctx.send("hey")

    @roll_54.error
    @roll_75.error
    async def info_error(self, ctx, error):
	    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
	        await ctx.send('Usage: [!50|!54|!75] [rs3|07] amount')