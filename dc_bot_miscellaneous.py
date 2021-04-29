from discord.ext import commands
from dc_bot_common import *
import time

class Miscellaneous(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.stop_val = False
    
    @commands.command()
    async def best(self,ctx):
        await ctx.send(f'{format(admin_id)} is the best!!!')
    
    @commands.command()
    async def hug(self,ctx):
        for usr in ctx.message.mentions:
            await ctx.send(f"hugs {format(usr.mention)}")
    
    @commands.command()
    async def kill(self,ctx):
        for usr in ctx.message.mentions:
            await ctx.send(f"Ok {format(usr.mention)} prepare to die!")
            
    @commands.command()
    async def stop(self,ctx):
        self.stop_val = not self.stop_val
        if self.stop_val: await ctx.send("Stop")
        else: await ctx.send("Resume")
            
    # todo maybe some real alarm :D
    @commands.command(brief='Try it on someone',
                description='Will tag taged users n times.\n\
                            Usage: "alarm 10 @user1 @user2"')
    async def alarm(self,ctx, n: int = 10):
        message = "Vstávej {}!!!"
        
        #handle extremes 
        max_ct = 20
        if (n > max_ct ): n = max_ct
        elif (0 > n): n = 0
        
        if (ctx.message.mentions == []):
            await ctx.send("Require to mention someone")
            return
        
        for i in range(n):
            for usr in ctx.message.mentions:
                await ctx.send(str(*message.format(usr.mention)))
                time.sleep(1)
            time.sleep(3)
            if (self.stop_val): break