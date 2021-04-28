# python3 dc_bot_main.py
# nohup python3 dc_bot_main.py 

from dc_bot_common import *

#? ---------------------------------------------------------
#! init
#? ---------------------------------------------------------

@bot.event
async def on_ready():
    print("INFO: Bot is ready")

@bot.event
async def on_message(ctx):
    # calling base method from discord extension
    await bot.process_commands(ctx)
    
    if ctx.author == bot.user:
        return

    # skipping if preffix in command
    if ctx.content == None or len(ctx.content) < 1 or ctx.content[0] in command_prefixes:
        return

    # checking bad words :D just because I can
    await on_profanity(ctx)

    # tts handling from tts channel
    await on_tts_message(ctx)
    
    # bot.dispatch('tts_message', ctx)
    # await bot.process_commands(ctx)
    
#? ---------------------------------------------------------
#! wellcome 
#? ---------------------------------------------------------

# todo create better message :D
@bot.event
async def on_member_join(member):
    print(f"{member.name} joined")
    await member.create_dm()
    await member.dm_channel.send(
        f'Nazdar {member.name}, nevim co chces u nas delat, ale vitej a bav se!!! XD XD XD'
    )

#? ---------------------------------------------------------
#! tts
#? ---------------------------------------------------------

# handling messages from tts channel
async def on_tts_message(ctx):
    if hasattr(ctx.author, 'voice') and ctx.author.voice is not None and ctx.author.voice.channel is not None:
        if('tts' in str(ctx.channel.name)):
            await tts_instance.say(ctx, ctx.content)

@bot.command(name='say', aliases=['s'])
async def say(ctx,  *, msg):
    await tts_instance.say(ctx, msg)

@bot.command()
async def lang(ctx, value: str = 'cs'):
    tts_instance.lang(value)

@bot.command()
async def volume(ctx, value: float):
    tts_instance.volume(value)
    
@bot.command()
async def tts_info(ctx):
    await tts_instance.info(ctx)
    
#? ---------------------------------------------------------
#! channel edit commands
#? ---------------------------------------------------------

# todo add command to delete all messages in channel
@bot.command(name='del')
async def delete(ctx, count: int = 100):
    deleted = await ctx.channel.purge(limit=count)
    await ctx.send(f"Deleted {len(deleted)} messages")

#? ---------------------------------------------------------
#! random commands                                              
# todo                                              add more                                         
#? ---------------------------------------------------------

async def on_profanity(ctx):
    # searching for bad words
    words = []
    for word in badwords:
        if word in ctx.content:
            words.append(word)
    if words == []:
        return

    await ctx.channel.send(f"{ctx.author.mention} Don't use that word!")
    embed = discord.Embed(title="Profanity Alert!",description=f"{ctx.author.name} just said ||{words}||", color=discord.Color.blurple()) # Let's make an embed!
    await ctx.channel.send(embed=embed)

#? ---------------------------------------------------------
#! tag commands
#? ---------------------------------------------------------

@bot.command()
async def stop(ctx):
    global stop_val
    stop_val = not stop_val
    if stop_val: await ctx.send(f"Stop")
    else: await ctx.send(f"Resume")

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
            sleep(1)
        sleep(3)
        if (stop_val): break

#? ---------------------------------------------------------
#! aka home assisstant
#? ---------------------------------------------------------

# my private function to control leds at home :D
# todo make it universal etc.
@bot.command(name='leds')
@commands.is_owner()
async def leds(ctx, r: int = 0, g: int = 0, b: int = 0):
    await ctx.send(f"Setting leds")
    cmd_arg = f'python3 ~/table_control/table_control.py -r {r} -g {g} -b {b}'
    child = subprocess.Popen(cmd_arg, shell=True)


#? ---------------------------------------------------------
#! debug
#? ---------------------------------------------------------

@bot.command(brief='Bot shutdown :(',
            description='Will shutdown bot compleately')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(f"Shutting down")
    log_error(f"Shutdown using command by {ctx.author.name}.")
    await ctx.bot.close()

@bot.command(brief='Bot restart :/',
            description='Will restart bot. And apply changes in source code.',
            aliases=['r'])
async def reboot(ctx):
    await ctx.send(f"Rebooting")
    log_error(f"Restart using command by {ctx.author.name}.")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    await ctx.bot.close()

@bot.command()
async def get_logs(ctx):
    channel = await get_bots_channel(ctx)
    await ctx.send(f"Sending logs into my channel: {channel}.")

    await channel.send(f"{now()} => log files:")
    for file in log_files:

        # check file existence
        if not path.exists(file):
            await channel.send((f'Log file "{file}" does not exist.'))
            continue
        
        # make it .txt to let dc make preview of it
        shutil.copy2(file, f'{file}.txt') 
        await channel.send(file = discord.File(f'{file}.txt'))
        try:
            os.remove(f'{file}.txt')
        except OSError as e:
            error_msg = f"Error: {e.filename} - {e.strerror}."
            log_error(error_msg)
            await channel.send(error_msg)

@bot.command()
@commands.is_owner()
async def del_logs(ctx):
    await ctx.send(f"Deleting log files")
    for file in log_files:
        # check file existence
        if not path.exists(file):
            await ctx.send((f'Log file "{file}" does not exist.'))
            continue

        try:
            os.remove(file)
            await ctx.send((f'Log file "{file}" deleted.'))
        except OSError as e:
            error_msg = f"Error: {e.filename} - {e.strerror}."
            log_error(error_msg)
            await ctx.send(error_msg)

#? ---------------------------------------------------------
#! error handeling
#? ---------------------------------------------------------

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
        if (ctx.author != None):
            log_error(error)

#? ---------------------------------------------------------
#! main
#? ---------------------------------------------------------

if __name__ == "__main__":
    bot.run(TOKEN)

    # called after bot.close