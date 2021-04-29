import discord
from discord.ext import commands
from discord.ext import tasks

from dc_bot_common import log_error, get_bots_channel, now
from dc_bot_data import data_class

import shutil
import sys
import os

data = data_class()

class debug_tools(commands.Cog):
    def __init__(self):
        pass
    
    @commands.command(brief='Bot shutdown :(',
                description='Will shutdown bot compleately')
    @commands.is_owner()
    async def shutdown(self,ctx):
        await ctx.send("Shutting down")
        log_error(f"Shutdown using command by {ctx.author.name}.")
        await ctx.bot.close()
    
    @commands.command(brief='Bot restart :/',
                description='Will restart bot. And apply changes in source code.',
                aliases=['r'])
    async def reboot(ctx):
        await ctx.send("Rebooting")
        log_error(f"Restart using command by {ctx.author.name}.")
        python = sys.executable
        os.execl(python, python, *sys.argv)
        await ctx.bot.close()
    
    @commands.command()
    @commands.is_owner()
    async def del_logs(self,ctx):
        log_files = [data.errlog_file]
        await ctx.send("Deleting log files")
        for file in log_files:
            # check file existence
            if not os.path.exists(file):
                await ctx.send((f'Log file "{file}" does not exist.'))
                continue
    
            try:
                os.remove(file)
                await ctx.send((f'Log file "{file}" deleted.'))
            except OSError as e:
                error_msg = f"Error: {e.filename} - {e.strerror}."
                log_error(error_msg)
                await ctx.send(error_msg)
                
    @commands.command()
    async def get_logs(self,ctx):
        log_files = [data.errlog_file]
        channel = await get_bots_channel(ctx)
        await ctx.send(f"Sending logs into my channel: {channel}.")
    
        await channel.send(f"{now()} => log files:")
        for file in log_files:
    
            # check file existence
            if not os.path.exists(file):
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