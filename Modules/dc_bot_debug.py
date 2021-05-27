import discord
from discord.ext import commands
from discord.ext import tasks

from Modules.dc_bot_common import log_error, now

import shutil
import sys
import os

class Debug_tools(commands.Cog):
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
    
    @commands.command(brief='Bot shutdown :(',
                description='Will shutdown bot completely')
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down")
        log_error(f"Shutdown using command by {ctx.author.name}.")
        await ctx.bot.close()
    
    @commands.command(brief='Bot restart :/',
                description='Will restart bot. And apply changes in source code.',
                aliases=['r'])
    async def reboot(self, ctx):
        await ctx.send("Rebooting")
        log_error(f"Restart using command by {ctx.author.name}.")
        python = sys.executable
        os.execl(python, python, *sys.argv)
        await ctx.bot.close()
    
    @commands.command()
    @commands.is_owner()
    async def del_logs(self,ctx):
        log_files = [self.data.errlog_file]
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
        
        log_files = [self.data.errlog_file]
        channel = self.bot.get_channel(self.data.channel_id)
        if not channel:
            channel = ctx

        await ctx.send("Sending logs into my channel.")
    
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