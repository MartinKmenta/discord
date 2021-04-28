# python3 dc_bot_main.py
# nohup python3 dc_bot_main.py 

from dc_bot_imports import *
from dc_bot_common import *
from dc_bot_tts import tts

with open('data.json') as data_json_file:
    data = json.load(data_json_file)

stop_val = False

command_prefixes = ['\\', '.', '?', '~', '/']

tts_instance = tts()

# admin#1234
admin_name = data["admin_name"]
# <@123123123123>
admin_id = data["admin_id"]

TOKEN = data["bot_token"]
bot = commands.Bot(command_prefix = command_prefixes)

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
    if ctx.content == None or ctx.content[0] in command_prefixes:
        return

    # tts handling from tts channel
    await tts_on_message(ctx)
    
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
async def tts_on_message(ctx):
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

# todo add command to delete all messages in chanel
@bot.command(name='del')
async def delete(ctx, count: int = 100):
    deleted = await ctx.channel.purge(limit=count)
    await ctx.send(f"Deleted {len(deleted)} messages")

#? ---------------------------------------------------------
#! tag commands
#? ---------------------------------------------------------

@bot.command()
async def stop(ctx):
    await ctx.send(f"Stopping")
    global stop_val
    stop_val = True
    # todo stop all activity such as tagging :D

# todo make it better to skip this command
# (I am too lazy now)
@bot.command()
async def resume(ctx):
    await ctx.send(f"Resuming")
    global stop_val
    stop_val = False
    # todo resume all activity such as tagging :D

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