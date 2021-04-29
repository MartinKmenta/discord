import discord
from discord.ext import commands
from discord.ext import tasks

import requests


class Games(commands.Cog):
    def __init__(self):
        #self.bot = bot
        self.games_expiring = []
        self.games_unknown_expiry = []
        
    def cog_unload(self):
        self.printer.cancel()
    
    def __repr__(self):
        return ""
    
    
    @tasks.loop(hours = 12)
    async def printer(self):
        pass
        
    def printer_debug(self,message):
        for x in message:
            print(x)
    
    def gamess(self):
        r = requests.get(url = "https://isthereanydeal.com/specials/#/filter:&giveaway")

        if r.status_code != 200:
            print(f"Server returned {r.status_code}")
            return 

        html = r.text[r.text.find('<div id=\'games\'>') : r.text.find('<div id="lazyload">')]
        games = html.split("bundle-container-outer")
        self.games_expiring = [ x for x in games if "left" in x ]
        self.games_unknown_expiry = [ x for x in games if "unknown expiry" in x ]
        

    def message_output(self):
        # message is 
        message = []
        games_expiring_steam = [ x for x in self.games_expiring if "https://store.steampowered." in x ]
        games_expiring_epic = [ x for x in self.games_expiring if "https://www.epicgames." in x ]
        
        if self.games_expiring == None or len(games_expiring_steam) == 0:
            message.append("No games found :cry:")        

        # steam games
        if games_expiring_steam != None and len(games_expiring_steam) > 0:
            message.append("Games on steam:")
            for g in games_expiring_steam:
                self.games_expiring.remove(g)
                g = g[g.find('bundle-time') : ]
                time_to_expire = g[g.find('>') + 1 : g.find('<')]
                g = g[g.find('href') : ]
                link = g[6 : g.find("class") - 2]
                title = g[g.find('>') + 1 : g.find('<')]

                message.append(f"{title}    {time_to_expire}    {link}")

        message.append("----------------------------------------------------")

        # epic games
        if games_expiring_epic != None and len(games_expiring_epic) > 0:
            message.append("Games on epic:")
            for g in games_expiring_epic:
                self.games_expiring.remove(g)
                g = g[g.find('bundle-time') : ]
                time_to_expire = g[g.find('>') + 1 : g.find('<')]
                g = g[g.find('href') : ]
                link = g[6 : g.find("class") - 2]
                title = g[g.find('>') + 1 : g.find('<')]

                message.append(f"{title}    {time_to_expire}    {link}")

        message.append("----------------------------------------------------")

        # other games
        if self.games_expiring != None and len(self.games_expiring) > 0:
            message.append("Other games:")
            for g in self.games_expiring:
                g = g[g.find('bundle-time') : ]
                time_to_expire = g[g.find('>') + 1 : g.find('<')]
                g = g[g.find('href') : ]
                link = g[6 : g.find("class") - 2]
                title = g[g.find('>') + 1 : g.find('<')]

                message.append(f"{title}    {time_to_expire}    {link}")
        
        self.printer_debug(message)
        return message