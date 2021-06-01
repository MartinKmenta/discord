import discord
from discord.ext import commands
from discord.ext import tasks

import requests
from bs4 import BeautifulSoup

import json

class Games(commands.Cog):
    """Inspired by https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html,
    https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html"""
    
    def __init__(self, bot = None, data = None):
        self.bot = bot
        self.data = data
        self.games_data = {}
        self.message = []
        self.output_file = "Resources/game_findings.json"
        self.printer.start()
        self.names = ["steam",
                      "epic",
                      "daily indie gaming",
                      "humble bundle",
                      "other"
                      ]


    def cog_unload(self):
        self.printer.cancel()


    def __str__(self):
        return "\n".join(self.message)


    @tasks.loop(hours = 12)
    async def printer(self):
        # generate data etc...
        self.before_printing()
        
        # load default channel, handle it's existance
        default_channel = self.bot.get_channel(self.data.channel_id)

        if not default_channel:
            print("INFO: No default channel")
            return
        
        # send in multiple messages
        for part in self.message:
            await default_channel.send(part)
        
        # memory cleanup
        self.printer_is_done()


    def printer_is_done(self):
        # memory cleanup
        self.message.clear()
        self.games_data.clear()


    def before_printing(self):
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
        games_data = {key : list() for key in self.names}
        
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
            deal_url = a["href"]
            
            template["title"] = a.text
            template["time"] = time.text
            template["url"] = deal_url
            
            # group by domain
            deals_domains = {"https://store.steampowered.com/" : "steam",
                             "https://www.epicgames.com/store/" : "epic",
                             "https://www.dailyindiegame.com" : "daily indie gaming",
                             "https://www.humblebundle.com" : "humble bundle",
                             "" : "other"
                             }
            
            # convert domain to simplified name
            for dkey in deals_domains:
                if deal_url.startswith(dkey):
                    key = deals_domains[dkey]
                    break
                
            # write to data
            games_data[key].append(template.copy())
            
        self.games_data = games_data

    
    def generate_message(self):
        # messages - list of string - stores readable lines
        full_message = []
        partial_message = ''
        mlines = []
        
        category_separator = 60*"-"
        
        # for all data, generate readable message.
        for key,games in self.games_data.items():
            mlines.append(category_separator)
            mlines.append(key)
            mlines.append(category_separator)
                        
            for game in games:
                line = "{}\t{}\t<{}>".format(*game.values())
                mlines.append(line)
        
        # group messages
        max_length = 1500
        sub_total = 0
        for line in mlines:
            sub_total += len(line) + 1
            partial_message += line + '\n'
            
            if sub_total > max_length:
                sub_total = 0
                full_message.append(partial_message)
                partial_message = ''
        
        self.message = full_message
    
    
    def write_to_json(self):
        with open(self.output_file,"w+") as out_file:
            json.dump(self.games_data, out_file, indent = 4)


    def load_json(self):
        with open(self.output_file,"r") as in_file:
            return json.load(in_file)
