from discord.ext import commands

class Amount(commands.Converter):
    async def convert(self, ctx, argument):
	    try:
	        char = argument[-1:].lower()
	        cases = {
	            'k': lambda num : float(num[0:-1]) * 1000,
	            'm': lambda num : float(num[0:-1]) * 1000000,
	            'b': lambda num : float(num[0:-1]) * 1000000000,
	        }
	        return cases.get(char, lambda num : float(num) * 1000000)(argument)
	    except ValueError:
	        raise BadArgument(f"Can't convert {argument} to a number.")

