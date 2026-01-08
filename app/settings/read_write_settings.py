import json

class Settings():
    def __init__(self):
        pass

    def read_settings(self, val):
        with open('settings.json', 'r') as f:
            data = json.load(f)
            print(data[val])

    def write_settings(self, item, val):
        with open('settings.json', 'r') as f:
            data = json.load(f)

        data[item] = val
        
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)

