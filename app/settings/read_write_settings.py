import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

class Settings():
    def __init__(self):
        pass

    def read_settings(self, val):
        with open(SETTINGS_PATH, 'r') as f:
            data = json.load(f)
            print(data[val])

    def write_settings(self, item, val):
        with open(SETTINGS_PATH, 'r') as f:
            data = json.load(f)

        data[item] = val
        
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(data, f, indent=4)

