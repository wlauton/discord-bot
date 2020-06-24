import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl
import requests
import asyncio


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
        try: requests.get("".join(arg))
        except: arg = " ".join(arg)
        else: arg = "".join(arg)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            
        embed = (discord.Embed(title='🎵 Musique en cours :', description=f"{info['title']}", color=discord.Color.blue())
                 .add_field(name='Durée', value=Music.parse_duration(info['duration']))
                 .add_field(name='Démandée par', value=author)
                 .add_field(name='Auteur', value=f"[{info['uploader']}]({info['channel_url']})")
                 .add_field(name='URL', value=f"[Lien vers la vidéo]({info['webpage_url']})")
                 .set_thumbnail(url=info['thumbnail']))
        
        return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title'], 'duration': info['duration']}

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue) > 1:
            del self.song_queue[0]
            voice.play(discord.FFmpegPCMAudio(self.song_queue[0]['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
            asyncio.run_coroutine_threadsafe(ctx.send(embed=self.song_queue[0]['embed'], delete_after=self.song_queue[0]['duration']), self.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)

    @commands.command(aliases=['p'], brief='!play [url/mots-clés]', description='Joue la musique demandée')
    async def play(self, ctx, *arg):
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)

        if channel:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            song = self.search(ctx.author.mention, arg)
            self.song_queue.append(song)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            if not voice.is_playing():
                voice.play(discord.FFmpegPCMAudio(self.song_queue[0]['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
                voice.is_playing()
                await ctx.send(embed=song['embed'], delete_after=song['duration'])
            else:
                await ctx.send(f":white_check_mark: Musique **{song['title']}** ajoutée à la file d'attente ({len(self.song_queue)-1} en attente)", delete_after = self.song_queue[0]['duration'])
        else:
            await ctx.send("❌ Tu n'es connecté à aucun channel !", delete_after = 5.0)

    @commands.command(aliases=['q'], brief="!queue", description="Affiche la file d'attente")
    async def queue(self, ctx):
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        embed = discord.Embed(color=discord.Color.blue(), title="⏱️ Liste d'attente :")
        if voice and voice.is_playing():
            for i in self.song_queue:
                if self.song_queue.index(i) == 0:
                    embed.add_field(name=f'**🔴 En cours :**', value=f"{i['title']}", inline=False)
                else:
                    embed.add_field(
                        name=f'**🎵 Track n°{self.song_queue.index(i)} :**', value=f"{i['title']}", inline=False)
            await ctx.send(embed=embed, delete_after = self.song_queue[0]['duration'])
        else:
            await ctx.send("❌ Je ne joue aucune musique !", delete_after = 5.0)

    @commands.command(brief='!pause', description='Met en pause ou reprend la musique en cours de lecture')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)
        if voice and voice.is_connected():
            if voice.is_playing():
                await ctx.send('⏸️ Musique en pause', delete_after = 5.0)
                voice.pause()
            else:
                await ctx.send('⏯️ Reprise de la musique', delete_after = 5.0)
                voice.resume()
        else:
            await ctx.send("❌ Je ne suis connecté à aucun channel !", delete_after = 5.0)

    @commands.command(aliases=['s', 'pass'], brief='!skip', description='Skip la musique en cours')
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)
        if voice and voice.is_playing():
            await ctx.send('⏭️ Music skippée', delete_after = 5.0)
            voice.stop()
        else:
            await ctx.send("❌ Je ne joue aucune musique !", delete_after = 5.0)

def setup(bot):
    bot.add_cog(Music(bot))
