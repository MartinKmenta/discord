import discord
from discord.ext import commands

from dc_bot_games import Games
from dc_bot_tts import Tts
from dc_bot_miscellaneous import Miscellaneous
from dc_bot_home_ctr import Home_Control
from dc_bot_data import Data_class
from dc_bot_debug import Debug_tools
from dc_bot_common import log_error

#? ---------------------------------------------------------
#! init
#? ---------------------------------------------------------

data = Data_class()

bot = commands.Bot(command_prefix = data.command_prefixes)


bot.add_cog(Games(bot, data))
bot.add_cog(Tts(bot))
bot.add_cog(Miscellaneous(bot))
bot.add_cog(Home_Control(bot))
bot.add_cog(Debug_tools(bot,data))


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
    if ctx.content == None or len(ctx.content) < 1 or ctx.content[0] in data.command_prefixes:
        return

    # checking bad words :D just because I can
    await on_profanity(ctx)    
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
    for word in data["badwords"]:
        if word in ctx.content:
            words.append(word)
    if words == []:
        return

    await ctx.channel.send(f"{ctx.author.mention} Don't use that word!")
    embed = discord.Embed(title="Profanity Alert!",
                          description=f"{ctx.author.name} just said ||{words}||",
                          color=discord.Color.blurple()) # Let's make an embed!
    await ctx.channel.send(embed=embed)

#? ---------------------------------------------------------
#! error handeling
#? ---------------------------------------------------------

# todo make better handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send("Unauthorized!")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        print(error)
        
        # log miscelenaous errors
        if (ctx.author != None):
            log_error(error)

#? ---------------------------------------------------------
#! main
#? ---------------------------------------------------------

if __name__ == "__main__":
    bot.run(data.TOKEN)

    # called after bot.close