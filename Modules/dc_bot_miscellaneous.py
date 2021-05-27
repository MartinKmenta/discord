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
        self.reminder_is_running = False

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

    @commands.command(aliases = ['remind','reminder','timer'])
    async def remindme(self, ctx, minutes: int = 5):
        minutes = min(minutes,24*60*60)
        when = int(time.time() + minutes*60)

        #if next reminder is not empty push to priority queue
        if self.next: 
            heapq.heappush(self.reminders, (when, ctx))
        else:
            self.next = (when,ctx)
        
        #start reminder loop
        if not self.reminder_is_running:
            print("INFO: reminder started")
            self.reminder_is_running = True
            self.reminder.start()

    @tasks.loop(minutes = 1)
    async def reminder(self):
        #self.next is not empty/None
        t, ctx = self.next

        #if now is later than reminder
        if time.time() > t:
            await ctx.reply("!!!")

            #next reminder
            if self.reminders:
                self.next = heapq.heappop(self.reminders)
            else:
                print("INFO: reminder stoped")
                self.next = None
                self.reminder_is_running = False
                self.reminder.stop()
            
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

        s = " ".join(usr.mention for usr in ctx.message.mentions)
        for i in range(n):
            await ctx.send(message.format(s))
            time.sleep(3)
            if (self.stop_val): break #limit alarm
        
    @commands.command(name='del')
    async def delete(self, ctx, count: int = 100):
        deleted = await ctx.channel.purge(limit=count)
        await ctx.send(f"Deleted {len(deleted)} messages")
