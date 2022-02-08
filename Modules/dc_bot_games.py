#  no longer needed becouse of https://github.com/FreeStuffBot/discord



# import discord
# from discord.ext import commands
# from discord.ext import tasks

# import requests
# from bs4 import BeautifulSoup

# import pandas as pd

# class Games(commands.Cog):
#     """Inspired by https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html,
#     https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html"""
    
#     def __init__(self, bot = None, data = None):
#         self.bot = bot
#         self.data = data
    
#         self.message = []
#         self.output_file = "Resources/game_findings.pkl"
#         self.printer.start()
#         self.printables = ["steam",
#                       "epic",
#                       "daily indie gaming",
#                       "humble bundle",
#                       "amazon",
#                       "indiegala",
#                       "jdoqocy",
#                       "other"
#                       ]

#         self.data = pd.DataFrame()
        
        
#     def cog_unload(self):
#         self.printer.cancel()


#     def __str__(self):
#         return "\n".join(self.message)

#     @tasks.loop(hours = 12)
#     async def printer(self):
        
#         # load default channel, handle it's existance
#         default_channel = self.bot.get_channel(self.data.channel_id)

#         if not default_channel:
#             print("INFO: No default channel")
#             return
        
#         # generate data etc...
#         self.before_printing()        
        
#         # send in multiple messages
#         for part in self.message:
#             await default_channel.send(part)
        
#         # memory cleanup
#         self.memory_cleanup()


#     def memory_cleanup(self):
#         # memory cleanup
#         self.message.clear()
#         self.games_data.clear()
#         self.raw_data.clear()


#     def before_printing(self):
#         # automation of updates and printing
#         self.find_new_games()
#         self.generate_message()


#     def find_new_games(self):
#         self.find_games()
#         try:
#             old_data = pd.read_pickle(filepath_or_buffer=self.output_file)
#         except:
#             print("no data found")
#         else:
#             new_data = pd.merge(self.data, old_data, on=['url'], how="outer", indicator=True)
#             new_data = new_data[new_data['_merge'] == 'left_only']
#             new_data.drop('_merge',1)
#             self.data = new_data
        
        
#     def find_games(self):
#         self.raw_find_games()
#         self.add_domain_name()
#         self.data.to_pickle(path=self.output_file)
    
    
#     def raw_find_games(self):
#         # request page data
#         page = requests.get(url = "https://isthereanydeal.com/specials/#/filter:&giveaway")
    
#         # handle errors
#         if page.status_code != 200:
#             print(f"Server returned {page.status_code}")
#             return 
      
#         # load page into BeautifulSoup, find containers
#         soup = BeautifulSoup(page.content, 'html.parser')
#         div_games = soup.find(id="games")
#         games_container = div_games.find_all(class_ = "bundle-container")
        
                
#         raw_data = []
        
#         # for all containers, find and write to data
#         for game in games_container:
#             # handle empty game, sholdn't occur
#             if game is None:
#                 continue
            
#             time = game.find(class_ = "bundle-time")
#             div_title = game.find(class_ = "bundle-title")
            
#             # handle time not found
#             if time is None:
#                 continue
            
#             # handle title not found
#             if div_title is None:
#                 continue
            
#             # fill template
#             a = div_title.select_one("a")
#             deal_url = a["href"]
            
#             raw_data.append((a.text,
#                              deal_url,
#                              time.text))
        
#         self.data = pd.DataFrame([*raw_data],columns=["name","url","time"])
#         self.data = self.data.drop_duplicates(subset=['url'],keep='first')
    
    
#     def add_domain_name(self):
#         def get_simplified_domain(url):    
#             # group by domain
#             deals_domains = {"https://store.steampowered.com/" : "steam",
#                              "https://www.epicgames.com/store/" : "epic",
#                              "https://www.dailyindiegame.com" : "daily indie gaming",
#                              "https://www.humblebundle.com" : "humble bundle",
#                              "https://gaming.amazon.com" : "amazon",
#                              "https://freebies.indiegala.com": "indiegala",
#                              "http://www.jdoqocy.com" : "jdoqocy",
#                              "" : "other"
#                              }
            
#             # convert domain to simplified name
#             for domain in deals_domains:
#                 if url.startswith(domain):
#                     key = deals_domains[domain]
#                     return key
        
#         self.data['domain'] = self.data.apply(lambda x: get_simplified_domain(x['url']),axis = 1)
    
    
#     def generate_message(self):
#         # messages - list of string - stores readable lines
#         full_message = []
#         partial_message = ''
#         mlines = []
#         category_separator = 60*"-"
        
        
#         grouped = self.data.groupby('domain')
#         for name in self.printables:
#             if name in grouped.groups:
#                 mlines.append(category_separator)
#                 mlines.append(name)
#                 mlines.append(category_separator)
                
#                 for i,s  in grouped.get_group(name).iterrows():
#                     line = "{}\t{}\t<{}>".format(*s[['name','time','url']])
#                     mlines.append(line)
        
#         max_length = 1500
#         sub_total = 0
#         for line in mlines:
#             sub_total += len(line) + 1
#             partial_message += line + '\n'
            
#             if sub_total > max_length:
#                 sub_total = 0
#                 full_message.append(partial_message)
#                 partial_message = ''
        
#         self.message = full_message
    
    
    
    
