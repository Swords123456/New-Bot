import discord
import config
from discord.ext import commands
from Rolls import Rolls

client = commands.Bot(command_prefix="!");


client.add_cog(Rolls(client))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if __name__  == '__main__':
	client.run(config.token)