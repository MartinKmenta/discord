import discord
from discord.ext import commands, tasks
import pprint

from Modules.dc_bot_games import Games
from Modules.dc_bot_tts import Tts
from Modules.dc_bot_miscellaneous import Miscellaneous
from Modules.dc_bot_home_ctr import Home_Control
from Modules.dc_bot_data import Data_class
from Modules.dc_bot_debug import Debug_tools
from Modules.dc_bot_common import log_error

#? ---------------------------------------------------------
#! init
#? ---------------------------------------------------------

data = Data_class()

bot = commands.Bot(command_prefix = data.command_prefixes)


bot.add_cog(Games(bot, data))
bot.add_cog(Tts(bot))
bot.add_cog(Miscellaneous(bot, data))
bot.add_cog(Home_Control(bot))
bot.add_cog(Debug_tools(bot,data))

separator = '-'*30

@bot.event
async def on_ready():
    print("INFO: Bot is ready")
    print(separator)
    pprint.pprint(data)
    print(separator)

    
@bot.command(name="join")
async def default_channel(ctx):
    global data
    data.channel_id = ctx.channel.id
    data.write_data()
    print(f"INFO: joined {data.channel_id}")
   
#? ---------------------------------------------------------
#! wellcome 
#? ---------------------------------------------------------

# todo create better message :D
@bot.event
async def on_member_join(member):
    print(f"{member.name} joined")
    await member.create_dm()
    await member.dm_channel.send(
        f'Nazdar {member.name}, nevím co chceš u nás dělat, ale vítej a bav se!!! XD XD XD'
    )

#? ---------------------------------------------------------
#! error handeling
#? ---------------------------------------------------------

# todo make better handeling
@bot.event
async def on_command_error(ctx, error):            
    if isinstance(error, commands.errors.CommandNotFound):
        return
    
    if __debug__:
        await bot.close()
        raise error
        
    print(separator)
    print(error)
    
    # log miscelenaous errors
    log_error(error)

#? ---------------------------------------------------------
#! main
#? ---------------------------------------------------------

if __name__ == "__main__":
    bot.run(data.TOKEN)
    # called after bot.close
    data.write_data()
