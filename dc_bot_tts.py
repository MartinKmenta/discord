from dc_bot_imports import *

class tts():

    def __init__(self):
        self.lang_str = 'cs'
        self.volume_val = 1.0

# todo make it jump into correct chanel
    async def say(self, ctx, msg):
        # todo make stack with messages ...
        # todo jump into correct chanel

        # create voice tack to say
        s = gTTS(text = msg, lang = self.lang_str, slow = False)
        s.save('tmp_files/tmp_dc_audio_to_say.mp3')

        if hasattr(ctx.author, 'voice') and ctx.author.voice is not None and ctx.author.voice.channel is not None:
            voice_channel = ctx.author.voice.channel
            voice = ctx.channel.guild.voice_client
            if voice is None:
                voice = await voice_channel.connect()
            elif voice.channel != voice_channel:
                voice.move_to(voice_channel)

            voice_raw = discord.FFmpegPCMAudio(source='tmp_files/tmp_dc_audio_to_say.mp3')
            if (self.volume_val != 1):
                voice.play(discord.PCMVolumeTransformer(voice_raw, volume=self.volume_val), 
                    after=lambda e: print('done'))
            else:
                voice.play(voice_raw) #, after=lambda e: print('done'))
        else:
            # hmmmm
            await ctx.send(f"please enter channel") 


    def lang(self, value: str = 'cs'):
        self.lang_str = value

    def volume(self, value: float = 1):
        self.volume_val = value
        
    async def info(self, ctx):
        await ctx.send(f"volume_val = {self.volume_val}")
        await ctx.send(f"lang_str = {self.lang_str}")