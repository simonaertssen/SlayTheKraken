import json
import requests

# read file
with open('../env/api_keys.json', 'r') as myfile:
    api_keys_data = myfile.read()

# parse file
API_KEY = json.loads(api_keys_data)

print(type(API_KEY))

r = requests.get('https://api.kraken.com/0/public/Time')
print(dir(r))
print(r.json())

r = requests.post('https://api.kraken.com/0/private/Balance')
print(dir(r))
print(r.json())