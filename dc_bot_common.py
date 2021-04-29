from dc_bot_tts import tts
from dc_bot_imports import *

# todo this :D
badwords = ['bad', 'wtf', 'prdele', 'vim']


with open('data.json') as data_json_file:
    data = json.load(data_json_file)

stop_val = False

command_prefixes = ['\\', '.', '?', '~', '/']
log_files = ['error.log', 'nohup.out']

# admin#1234
admin_name = data["admin_name"]
# <@123123123123>
admin_id = data["admin_id"]
# 123123123123123123123
channel_id_for_this_bot = int(data["channel_id_for_this_bot"])
channel_default_name_for_this_bot = data["channel_default_name_for_this_bot"]

TOKEN = data["bot_token"]

def now():
    return time.strftime("%a, %d %b %Y %H:%M:%S")

def log_error(error_msg):
    with open("error.log", "a") as error_logs:
        error_logs.write(now() + " => " + str(error_msg) + "\n")

async def get_bots_channel(ctx):
    global channel_id_for_this_bot

    channel = bot.get_channel(channel_id_for_this_bot)
    if channel != None:
        return channel

    # creating channel
    channel = await ctx.guild.create_text_channel(channel_default_name_for_this_bot)
    channel_id_for_this_bot = channel.id
    data["channel_id_for_this_bot"] = str(channel_id_for_this_bot)

    # savimg new channel id
    with open('data.json', 'w') as data_json_file:
        json.dump(data, data_json_file, indent = 4)

    return bot.get_channel(channel_id_for_this_bot)