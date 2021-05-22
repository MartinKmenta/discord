import json

class Data_class(dict):
    def __init__(self):
        self.file_name = "data.json"
        self.errlog_file = "error.log"
        
        with open('data.json') as data_json_file:
            data = json.load(data_json_file)
        
        super(Data_class,self).__init__(data)
    
    def __getattr__(self,key):
        return self[key]
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __del__(self):
        print("Destructor called, data saved.")
        self.write_data()
            
    def write_data(self):
        with open(self.file_name, mode = "w") as data_json_file:
            json.dump(self, data_json_file)