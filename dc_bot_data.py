import json

class Data_class():
    def __init__(self):
        self.file = "data.json"
        self.errlog_file = "error.log"
        
        with open('data.json') as data_json_file:
            self.data = json.load(data_json_file)
        
        # for Martin Kmenta because he doesn't like dictionaries
        # doesn't update data
        self.command_prefixes = self.data["command_prefixes"]
        self.admin_id = self.data["admin_id"]
        self.admin_name = self.data["admin_name"]
        self.TOKEN = self.data["TOKEN"]
        self.channel_id = self.data["channel_id"]
        self.server_id = self.data["server_id"]
        self.channel_default_name_for_this_bot = self.data["channel_default_name_for_this_bot"]
        self.badwords = self.data["badwords"]
        

        # todo loading from file and storing info about changes
        
    def update_data(self):
        with open('data.json') as data_json_file:
            json.dump(self.data, data_json_file)
    
    