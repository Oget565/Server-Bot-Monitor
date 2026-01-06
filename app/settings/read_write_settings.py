import json

def read_settings(val):
    with open('settings.json', 'r') as f:
        data = json.load(f)
        print(data[val])

def write_settings(item, val):
    with open('settings.json', 'r') as f:
        data = json.load(f)

    data[item] = val
    
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=4)

read_settings("timezone")
write_settings("update_interval", 5)