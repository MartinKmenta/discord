from dc_bot_common import *
from dc_bot_games import Games
from dc_bot_tts import tts
from dc_bot_miscellaneous import Miscellaneous

#? ---------------------------------------------------------
#! init
#? ---------------------------------------------------------
bot = commands.Bot(command_prefix = command_prefixes)
channel = bot.get_channel(channel_id_for_this_bot)
bot.add_cog(Games(bot,default_channel= channel))
bot.add_cog(tts(bot))
bot.add_cog(Miscellaneous(bot))


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