from discord.ext import commands
import subprocess

class Home_Control(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def leds(self, ctx, r: int = 0, g: int = 0, b: int = 0):
        await ctx.send("Setting leds")
        cmd_arg = f'python3 ~/table_control/table_control.py -r {r} -g {g} -b {b}'
        child = subprocess.Popen(cmd_arg, shell=True)
    
