import discord
from discord.ext import commands, tasks
from datetime import datetime
import heapq
import time

class Miscellaneous(commands.Cog):
    def __init__(self,bot,data):
        self.bot = bot
        self.stop_val = False
        self.data = data
        self.reminders = []
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

    def format_time_for_reminder(self, time):
        # UTC + 1h
        timezone = 3600
        return datetime.fromtimestamp(time + timezone).strftime('at %H:%M on %d. %m. %Y')

    @commands.command(aliases = ['timers'])
    async def reminders(self, ctx):
        await ctx.send("```reminders:\n" + ("\n".join(f"{self.format_time_for_reminder(when)} {ctx.author}" for when, ctx in self.reminders)) + "```")

        

    @commands.command(aliases = ['remind','reminder','timer','responce'])
    async def remindme(self, ctx, minutes: int = 5, hours: int = 0, days: int = 0):
        minutes += (days * 24 + hours) * 60
        max_42_days = 24 * 60 * 42
        if minutes > max_42_days:
            minutes = max_42_days
            await ctx.reply("Maximal time is 42 days")
            
        when = int(time.time() + minutes * 60)

        await ctx.reply(f"Ok, {self.format_time_for_reminder(when)}")

        self.reminders.append((when, ctx))
        self.reminders.sort(key=lambda x: x[0])
        
        #start reminder loop
        if not self.reminder_is_running:
            # print("INFO: reminder started")
            self.reminder_is_running = True
            self.reminder.start()


    @tasks.loop(minutes = 1)
    async def reminder(self):
        #if now is later than reminder
        # first reminder is the most actual and first element in tuple is time
        while self.reminders and time.time() > self.reminders[0][0]:
            _, ctx = self.reminders.pop(0)
            try:
                await ctx.reply(f"!!! {ctx.author.mention}")
            except:
                await ctx.send(f"!!! {ctx.author.mention}")

        if self.reminder_is_running and not self.reminders:
            # print("INFO: reminder stoped")
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


    async def on_profanity(self,message):
        # searching for bad words
        words = []
        for word in self.data["badwords"]:
            if word.lower() in message.content:
                words.append(word)
        if words == []:
            return
    
        await message.channel.send(f"{message.author.mention} Don't use that word!")
        embed = discord.Embed(title="Profanity Alert!",
                              description=f"{message.author.name} just said ||{words}||",
                              color=discord.Color.blurple()) # Let's make an embed!
        await message.channel.send(embed=embed)
