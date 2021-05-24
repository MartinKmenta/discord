from discord.ext import commands, tasks
import heapq
import time

class Miscellaneous(commands.Cog):
    def __init__(self,bot,data):
        self.bot = bot
        self.stop_val = False
        self.data = data
        self.reminders = []
        self.next = None
    
        self.reminder.start()

    @commands.command()
    async def best(self, ctx):
        await ctx.send(f'{self.data.admin_id} is the best!!!')
    
    @commands.command()
    async def hug(self, ctx):
        for usr in ctx.message.mentions:
            await ctx.send(f"hugs {usr.mention}")
    
    @commands.command()
    async def kill(self, ctx):
        for usr in ctx.message.mentions:
            await ctx.send(f"Ok {usr.mention} prepare to die!")
            
    @commands.command()
    async def stop(self, ctx):
        self.stop_val = not self.stop_val
        if self.stop_val: await ctx.send("Stop")
        else: await ctx.send("Resume")

    @commands.command()
    async def remindme(self, ctx, minutes: int = 5):
        when = int(time.time() + minutes*60)
        heapq.heappush(self.reminders, (when, ctx))

    @tasks.loop(minutes = 5)
    async def reminder(self):
        t, ctx = self.next
        if time.time() < t:
            ctx.send(f"!!! {ctx.author} !!!")
            self.next = heapq.pop(self.reminders)
            
    @commands.command(brief='Try it on someone',
                      description="Will tag taged users n times. \nUsage: alarm 10 @user1 @user2 ...")
    async def alarm(self, ctx, n: int = 10):
        message = "Vstávej {}!!!"
        
        #handle extremes 
        max_ct = 20
        if (n > max_ct ): n = max_ct
        elif (0 > n): n = 0
        
        if (ctx.message.mentions == []):
            await ctx.send("Requires to mention someone")
            return
        
        for i in range(n):
            for usr in ctx.message.mentions:
                await ctx.send(message.format(usr.mention))
                time.sleep(1)
            time.sleep(3)
            if (self.stop_val): break
        
    @commands.command(name='del')
    async def delete(ctx, count: int = 100):
        deleted = await ctx.channel.purge(limit=count)
        await ctx.send(f"Deleted {len(deleted)} messages")
