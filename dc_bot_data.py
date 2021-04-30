import json

class data_class():
    def __init__(self):
        self.file_name = "data.json"
        self.errlog_file = "error.log"
        
        with open('data.json') as data_json_file:
            self.data = json.load(data_json_file)
        
        # for Martin Kmenta because he doesn't like dictionaries
        # doesn't update data
        self.command_prefixes = self.data["command_prefixes"]
        self.admin_id = self.data["admin_id"]
        self.command_prefixes = ["."]
        self.admin_name = self.data["admin_name"]
        self.TOKEN = self.data["TOKEN"]
        self.channel_id_for_this_bot = self.data["channel_id_for_this_bot"]
        self.channel_default_name_for_this_bot = self.data["channel_default_name_for_this_bot"]

        
        
    def write_data(self):
        with open(self.file_name) as data_json_file:
            json.dump(self.data, data_json_file)
    
    def fetch_data(self):
        with open(self.file_name) as data_json_file:
            self.data = json.load(data_json_file)
