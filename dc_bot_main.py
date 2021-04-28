# python3 dc_bot_main.py
# nohup python3 dc_bot_main.py 

import discord
from discord.ext import commands
from discord.ext import tasks
import argparse
import subprocess
import json
import random
import subprocess
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import sys
import os

with open('data.json') as data_json_file:
    data = json.load(data_json_file)

# todo create object tts and store these values in config file together with alliases for user etc.
lang_str = 'cs'
volume_val = 1.0
stop_val = False

# admin#1234
admin_name = data["admin_name"]
# <@123123123123>
admin_id = data["admin_id"]

TOKEN = data["bot_token"]

# todo make it changeable
bot = commands.Bot(command_prefix=['\\', '.', '?', '~'])

# todo say every message in tts room
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     await message.channel.send(message.content)

# todo make chanel for this bot and let him print info and some allers such ase games with 100 % sale :D

@bot.event
async def on_ready():
    print("INFO: Bot is ready")

# todo create better message :D
@bot.event
async def on_member_join(member):
    print(f"{member.name} joined")
    await member.create_dm()
    await member.dm_channel.send(
        f'Nazdar {member.name}, nevim co chces u nas delat, ale vitej a bav se!!! XD XD XD'
    )

# todo add command to delete all messages in chanel
@bot.command(name='del')
async def delete(ctx, count: int = 100):
    deleted = await ctx.channel.purge(limit=count)
    await ctx.send(f"Deleted {len(deleted)} messages")

# my private function to control leds at home :D
# todo make it universal etc.
@bot.command(name='leds')
@commands.is_owner()
async def leds(ctx, r: int = 0, g: int = 0, b: int = 0):
    await ctx.send(f"Setting leds")
    cmd_arg = f'python3 ~/table_control/table_control.py -r {r} -g {g} -b {b}'
    child = subprocess.Popen(cmd_arg, shell=True)

# todo make it jump into correct chanel
@bot.command(name='say', aliases=['s'])
async def say(ctx,  *, msg):
    # todo make stack with messages ...
    # await ctx.send(msg, tts=True)
    global gTTS
    s = gTTS(text = msg, lang = lang_str, slow = False)
    s.save('tmp_dc_audio_to_say.mp3')
    if hasattr(ctx.author, 'voice') and ctx.author.voice is not None and ctx.author.voice.channel is not None:
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice.move_to(voice_channel)

        voice_raw = discord.FFmpegPCMAudio(source='tmp_dc_audio_to_say.mp3')
        if (volume_val != 1):
            voice.play(discord.PCMVolumeTransformer(voice_raw, volume=volume_val), 
                after=lambda e: print('done'))
        else:
            voice.play(voice_raw, after=lambda e: print('done'))
    else:
        await ctx.send(f"please enter channel")

# todo make it inside object - global is bad :D
@bot.command()
async def lang(ctx, value: str = 'cs'):
    global lang_str
    lang_str = value

@bot.command()
async def volume(ctx, value: float):
    global volume_val
    volume_val = value
    
@bot.command()
async def info(ctx):
    await ctx.send(f"lang_str   = {lang_str}")
    await ctx.send(f"volume_val = {volume_val}")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(f"Shutting down")
    await ctx.bot.close()

@bot.command()
async def stop(ctx):
    global stop_val
    stop_val = not stop_val
    if stop_val: await ctx.send(f"Stop")
    else: await ctx.send(f"Resume")

@bot.command(aliases=['r'])
async def reboot(ctx):
    await ctx.send(f"Rebooting")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    exit(1)
    # rebooting no need to rubn it again if there are changes

@bot.command()
async def best(ctx):
    await ctx.send(f'{format(admin_id)} is the best!!!')

@bot.command()
async def hug(ctx):
    for usr in ctx.message.mentions:
        await ctx.send(f"hugs {format(usr.mention)}")

@bot.command()
async def kill(ctx):
    for usr in ctx.message.mentions:
        await ctx.send(f"Ok {format(usr.mention)} prepare to die!")

        
# todo maybe some real alarm :D
@bot.command(brief='Try it on someone',
            description='Will tag taged users n times.\n\
Usage: "alarm 10 @user1 @user2"')
async def alarm(ctx, n: int = 10):
    global stop_val
    message = "Vstávej {}!!!"
    
    #handle extremes 
    max_ct = 20
    if (n > max_ct ): n = max_ct
    elif (0 > n): n = 0
    
    if (ctx.message.mentions == []):
        await ctx.send(f"Require to mention someone")
        return
    
    for i in range(n):
        for usr in ctx.message.mentions:
            await ctx.send(message.format(usr.mention))
            time.sleep(1)
        time.sleep(3)
        if (stop_val): break

# todo make better handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send(f"Unauthorized!")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        await ctx.send(error)
        
        # log miscelenaous errors
        with open("error_logs.json","a") as error_logs:
            json.dump({time.strftime("%a, %d %b %Y %H:%M:%S") : error}, error_logs, indent=4)

if __name__ == "__main__":
    bot.run(TOKEN)
    # can't put anything here now
