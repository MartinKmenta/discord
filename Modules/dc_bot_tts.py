import discord
from discord.ext import commands

# for tts 
from mutagen.mp3 import MP3
from gtts import gTTS, lang

import time
import heapq

class Tts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.lang_str = 'cs'
        self.volume_val = 1.0
        self.is_active = False
        self.default_channel = None
        self.voice_channel = None
        self.joined = False
        self.tts_queue = []

    async def voice_channel_handeler(self,ctx):
        if not all(hasattr(ctx.author, 'voice'), ctx.author.voice, ctx.author.voice.channel):
            self.joined = False
            return

        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        
        if voice is None:
            voice = await voice_channel.connect()
            time.sleep(0.1)

        if voice.channel != voice_channel:
            await voice.move_to(voice_channel)
            # give some time to bot to find out where he is :D
            time.sleep(0.1)

        self.joined = True
        self.voice_channel = voice


    async def text_to_speech_save(self,msg):
        # create voice track to say
        s = gTTS(text = msg, lang = self.lang_str, slow = False)
        s.save('tmp_files/tmp_dc_audio_to_say.mp3')


    async def play_from_source():
        # playing autio file
        voice_raw = discord.FFmpegPCMAudio(source='tmp_files/tmp_dc_audio_to_say.mp3')

        # if volume is not 1 transform to volume
        if (self.volume_val != 1):
            voice_raw = discord.PCMVolumeTransformer(voice_raw, volume=self.volume_val)

        self.voice_channel.play(voice_raw)
    

    @commands.command(aliases = ['s'])
    async def say(self, ctx, *, msg):
        await self.voice_channel_handeler(ctx)
        
        if not self.joined:
            return

        await self.text_to_speech_save(msg)
        await self.play_from_source()


    @commands.Cog.listener()
    async def on_message(self,message):
        if not is_active:
            return

        if message.channel != self.default_channel:
            return


    @commands.command(description = " ".join(lang.tts_langs().keys()))
    async def lang(self, ctx, value: str = 'cs'):
        if value in lang.tts_langs():
            self.lang_str = value
            await ctx.send(f"Language set to {self.lang_str}")
            return

        await ctx.send(f"Invalid language => help lang")


    @commands.command()
    async def volume(self, ctx, value: float = 1):
        if value > 2 or value < 0:
            await ctx.send(f"Invalid value => 0 - 2")

            #handle extremes 
            max_ct = 2
            if (value > max_ct ): value = max_ct
            elif (0 > value): value = 0

        self.volume_val = value
        await ctx.send(f"Volume set to {self.volume_val}")

    
    @commands.command()
    async def info(self, ctx):
        await ctx.send(f"volume_val = {self.volume_val}")
        await ctx.send(f"lang_str = {self.lang_str}")
