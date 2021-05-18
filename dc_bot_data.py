import json

class data_class():
    def __init__(self):
        self.file_name = "data.json"
        self.errlog_file = "error.log"
        
        with open('data.json') as data_json_file:
            self.data = json.load(data_json_file)
        
        # unpack data to atributes
        for key,item in self.data.items():
            setattr(self, key, item)
        
        
    def write_data(self):
        with open(self.file_name) as data_json_file:
            json.dump(self.data, data_json_file)
    
    def fetch_data(self):
        with open(self.file_name) as data_json_file:
            self.data = json.load(data_json_file)
