import discord
from discord.ext import commands

# for tts 
# from mutagen.mp3 import MP3
from gtts import gTTS, lang
from io import BytesIO

import time
# import heapq

class Tts(commands.Cog):

    def __init__(self, bot = None):
        self.bot = bot
        self.lang_str = 'cs'
        self.volume_val = 1.0
        self.is_active = False
        self.default_channel = None
        self.voice_client = None
        self.joined = False
        self.tts_queue = []
        #self.voice = discord.VoiceClient(client, channel)
        

    async def tts_join(self,ctx):
        self.voice_channel_handeler(ctx.author)
        
    
    async def voice_channel_handeler(self,author):
        #join 
        voice_channel = author.voice.channel  
        voice_client = await voice_channel.connect()
        time.sleep(0.1)

        self.joined = True
        self.voice_client = voice_client
        print(self.voice_client)


    async def text_to_speech_save_to_file(self,msg: str):
        # create voice track to say
        s = gTTS(text = msg, lang = self.lang_str, slow = False)
        s.save('tmp_files/tmp_dc_audio_to_say.mp3')


    async def text_to_speech(self,msg: str):
        tts = gTTS(text = msg, lang = self.lang_str)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        return mp3_fp


    async def tts_play(self,msg: str):
        mp3_fp = await self.text_to_speech(msg)
        audio = discord.FFmpegAudio(source = mp3_fp)
        await self.voice_client.play(audio)


    async def play_from_source(self,path):
        # playing autio file
        voice_source = discord.FFmpegPCMAudio(source=path)

        # if volume is not 1 transform to volume
        if (self.volume_val != 1):
            voice_source = discord.PCMVolumeTransformer(voice_source, volume=self.volume_val)

        self.voice_channel.play(voice_source)
    

    @commands.command(aliases = ['s'])
    async def say(self, ctx, *, msg):
        await self.voice_channel_handeler(ctx.author)
        
        if not self.joined:
            return

        await self.tts_play(msg)


    @commands.Cog.listener()
    async def on_message(self,message):
        if not self.is_active:
            return

        if message.channel != self.default_channel:
            return

        await self.voice_channel_handeler(message.author)
        await self.tts_play(message.content)


    @commands.command(description = " ".join(lang.tts_langs().keys()))
    async def lang(self, ctx, value: str = 'cs'):
        if value in lang.tts_langs():
            self.lang_str = value
            await ctx.send(f"Language set to {self.lang_str}")
            return

        await ctx.send("Invalid language => help lang")


    @commands.command()
    async def volume(self, ctx, value: float = 1):
        if value > 2 or value < 0:
            await ctx.send("Invalid value => 0 - 2")

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
