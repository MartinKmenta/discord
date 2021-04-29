import discord
from discord.ext import commands
from discord.ext import tasks

import requests
from bs4 import BeautifulSoup

import json



class Games(commands.Cog):
    """Inspired by https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html,
    https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html"""
    
    def __init__(self,bot,default_channel):
        self.bot = bot
        self.default_channel = default_channel
        
        self.data = {}
        self.message = []
        
    def cog_unload(self):
        self.printer.cancel()
    
    def __str__(self):
        return "\n".join(self.message)
    
    @tasks.loop(hours = 12)
    async def printer(self):
        # automation of updates and printing
        self.find_games()
        self.generate_message()
        
        # send in multiple messages
        for line in self.message:
            self.default_channel.send(line)
            
    def find_games(self):
        # request page data
        page = requests.get(url = "https://isthereanydeal.com/specials/#/filter:&giveaway")
    
        # handle errors
        if page.status_code != 200:
            print(f"Server returned {page.status_code}")
            return 
      
        # load page into BeautifulSoup, find containers
        soup = BeautifulSoup(page.content, 'html.parser')
        div_games = soup.find(id="games")
        games_container = div_games.find_all(class_ = "bundle-container")
        
        # store games in dictionary: keys = "steam","epic", "other"
        data = {"steam":[],"epic":[],"other":[]}
        template = {"title": None, "time": None, "url": None}
        
        # for all containers, find and write to data
        for game in games_container:
            # handle empty game, sholdn't occur
            if game is None:
                continue
            
            time = game.find(class_ = "bundle-time")
            div_title = game.find(class_ = "bundle-title")
            
            # handle time not found
            if time is None:
                continue
            
            # handle title not found
            if div_title is None:
                continue
            
            # fill template
            a = div_title.select_one("a")
            template["title"] = a.text
            template["time"] = time.text
            template["url"] = a["href"]
            
            # group by page
            if "https://store.steampowered.com/" in a["href"]:
                key = "steam"
            elif "https://www.epicgames.com/store/" in a["href"]:
                key = "epic"
            else:
                key = "other"
            
            # write to data
            data[key].append(template.copy())
            
        self.data = data
        
    def generate_message(self):
        # messages - list of string - stores readable lines
        message = []
        # for all data, generate readable message.
        for key,games in self.data.items():
            message.append(key)
            message.append(30*"-")
            for game in games:
                message.append("{}\t{}\t{}".format(*game.values()))
            message.append(30*"-")
            
        self.message = message
                
    def write_to_json(self):
        with open("game_fingins.json","w") as out_file:
            json.dump(self.data, out_file, indent = 4)
                
                
                
                
                
                
                
                
                
                
                
                
                
                