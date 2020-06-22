import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
initial_extensions = [
    'cogs.music',
    'cogs.chat',
    'cogs.JDR',
    'cogs.random'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name='!help'))
    print(f'Bot is ready!')


bot.run('TOKEN', bot=True, reconnect=True)
