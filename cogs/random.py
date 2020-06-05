import discord
from discord.ext import commands

import random


class random(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='!toss [heads/tails]', description='Make a coin toss against the bot')
    async def pof(self, ctx, arg):
        piece = random.choice(['Tails', 'Heads'])
        if arg.upper() == 'PILE' or arg.upper() == 'TAILS':
            if arg.upper() == piece.upper():
                await ctx.send(f':white_check_mark: {piece} ! You won.')
            else:
                await ctx.send(f':negative_squared_cross_mark:  {piece} ! You lost.')
        else:
            await ctx.send('❌ You must input either "heads" or "tails"')

    @commands.command(brief='!poke [random/nickname]', description='Mention a member (randomly or not)')
    async def poke(self, ctx, arg):
        user = ''
        online_members = []
        for x in ctx.guild.members:
            if x.status == discord.Status.online and not x.bot:
                online_members.append(x)
            try:
                if x.name.lower().startswith(arg.lower()) or x.nick.lower().startswith(arg.lower()):
                    user = x
            except:
                pass
        if arg == 'random':
            user = random.choice(online_members).mention
            await ctx.send(f'Hey {user} !')
        elif user:
            await ctx.send(f'Hey {user.mention} !')
        else:
            await ctx.send('❌ You must input either "random" or an online member !')

def setup(bot):
    bot.add_cog(random(bot))
