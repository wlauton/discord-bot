import discord
from discord.ext import commands

class chat(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['delete', 'purge'], brief='!clear [x]', description='Deletes the [x] previous messages')
    async def clear(self, ctx, limit):
        try:
            float(limit)
        except:
            await ctx.send('❌ You must input an integer !')
        else:
            limit = int(limit) + 1
            await ctx.channel.purge(limit=limit)
    
    @commands.command(brief='!help [category/none]', description="Displays an help message")
    async def help(self, ctx, *c):
        if not c:
            await ctx.channel.purge(limit=1)
            temp = []
            embed = discord.Embed(color=discord.Color.blue(), title='Commands list :')
            for x in self.bot.cogs:
                for y in self.bot.get_cog(x).get_commands():
                    if not y.hidden:
                        temp.append(f"\n{y.brief}")
                embed.add_field(name=f'**{x} :**', value=f"{''.join(temp[0:len(temp)])}", inline=False)
                temp = []
            await ctx.send(embed=embed)
        elif len(c) == 1:
            c = ''.join(c[:])
            if self.bot.get_cog(c):
                await ctx.channel.purge(limit=1)
                embed = discord.Embed(color=discord.Color.blue(), title=f'Commands in "{c}" category')
                for x in self.bot.get_cog(c).get_commands():
                    if not x.hidden:
                        embed.add_field(name=f'**{x.brief} :**', value=f"{x.description}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Category name wasn't found !")
        else:
            await ctx.send("❌ You have to input only one category !")

def setup(bot):
    bot.add_cog(chat(bot))
