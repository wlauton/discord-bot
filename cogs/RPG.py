import discord
from discord.ext import commands

from random import randint

class RPG(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['zone', 'add_zone'], hidden=True)
    async def zones(self, ctx, *arg):
        if ctx.message.author == 'Mr_Spaar' or 'Marnic':
            if arg:
                embed = discord.Embed(color=discord.Color.blue(), title=":map: New forbidden zones :")
                embed.add_field(name=f'❌ {arg[1].upper()}', value=f':timer: {arg[0].upper()}')
                embed.add_field(name=f'❌ {arg[3].upper()}', value=f':timer: {arg[2].upper()}')
                embed.add_field(name='\u200b', value='<@&711644677517869137>', inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('❌ No new forbidden zones !')

    @commands.command(aliases=['r'], brief='!roll [x]', description='Simulates a dice roll')
    async def roll(self, ctx, arg):
        try:
            float(arg)
        except:
            await ctx.send('❌ You must input an integer !')
        else:
            number = randint(1, int(arg))
            await ctx.send(f'🎲 You rolled a {number} !')

def setup(bot):
    bot.add_cog(RPG(bot))
