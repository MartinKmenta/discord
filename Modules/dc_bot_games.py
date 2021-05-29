import discord
from discord.ext import commands
from discord.ext import tasks

import requests
from bs4 import BeautifulSoup

import json

class Games(commands.Cog):
    """Inspired by https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html,
    https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html"""
    
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.games_data = {}
        self.message = []
        self.output_file = "Resources/game_findings.json"
        self.printer.start()


    def cog_unload(self):
        self.printer.cancel()


    def __str__(self):
        return "\n".join(self.message)


    @tasks.loop(hours = 12)
    async def printer(self):
        default_channel = self.bot.get_channel(self.data.channel_id)

        if not default_channel:
            print("INFO: No default channel")
            return
        
        # send in multiple messages
        for line in self.message:
            await default_channel.send(line)


    @printer.after_loop
    async def printer_is_done(self):
        # memory cleanup
        self.message.clear()
        self.games_data.clear()


    @printer.before_loop
    async def before_printing(self):        
        # automation of updates and printing
        self.find_games()
        self.generate_message()
        
        # save data for later comparasion
        self.write_to_json()
    
    
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
        games_data = {"steam":[],
                      "epic":[],
                      "daily indie gaming":[],
                      "humble bundle":[],
                      "other":[]
                      }
        
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
            deal_url = a["href"]
            template["url"] = deal_url
            
            # group by domain
            deals_domains = {"https://store.steampowered.com/" : "steam",
                             "https://www.epicgames.com/store/" : "epic",
                             "https://www.dailyindiegame.com" : "daily indie gaming",
                             "https://www.humblebundle.com" : "humble bundle"
                             }
            
            key = "other"
            
            for dkey in deals_domains:
                if deal_url.startswith(dkey):
                    key = deals_domains[dkey]
                    break
                
            # write to data
            games_data[key].append(template.copy())
            
        self.games_data = games_data

    
    def generate_message(self):
        # messages - list of string - stores readable lines
        message = []
        category_separator = 60*"-"
        # for all data, generate readable message.
        for key,games in self.games_data.items():
            message.append(key)
            message.append(category_separator)
            for game in games:
                message.append("{}\t{}\t<{}>".format(*game.values()))
            message.append(category_separator)
            
        self.message = message
    
    
    def write_to_json(self):
        with open(self.output_file,"w+") as out_file:
            json.dump(self.games_data, out_file, indent = 4)


    def load_json(self):
        with open(self.output_file,"r") as in_file:
            return json.load(in_file)
