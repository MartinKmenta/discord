import discord
from discord.ext import commands

# for tts 
from mutagen.mp3 import MP3
from gtts import gTTS

import time

class tts(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.lang_str = 'cs'
        self.volume_val = 1.0
    
    @commands.command()
    async def say(self, ctx, msg):
        # todo make stack with messages ...

        # create voice tack to say
        s = gTTS(text = msg, lang = self.lang_str, slow = False)
        s.save('tmp_files/tmp_dc_audio_to_say.mp3')

        if hasattr(ctx.author, 'voice') and ctx.author.voice is not None and ctx.author.voice.channel is not None:
            voice_channel = ctx.author.voice.channel
            voice = ctx.channel.guild.voice_client
            if voice is None:
                voice = await voice_channel.connect()
                time.sleep(0.1)
            if voice.channel != voice_channel:
                await voice.move_to(voice_channel)
                # give some time to bot to find out where he is :D
                time.sleep(0.1)

            # playing autio file
            voice_raw = discord.FFmpegPCMAudio(source='tmp_files/tmp_dc_audio_to_say.mp3')
            if (self.volume_val != 1):
                voice.play(discord.PCMVolumeTransformer(voice_raw, volume=self.volume_val), 
                    after=lambda e: print('done'))
            else:
                voice.play(voice_raw) #, after=lambda e: print('done'))
        else:
            await ctx.send("please enter channel") 
    
    @commands.command()
    async def lang(self, value: str = 'cs'):
        self.lang_str = value
        
    @commands.command()
    async def volume(self, value: float = 1):
        self.volume_val = value
    
    @commands.command()
    async def info(self, ctx):
        await ctx.send(f"volume_val = {self.volume_val}")
        await ctx.send(f"lang_str = {self.lang_str}")
