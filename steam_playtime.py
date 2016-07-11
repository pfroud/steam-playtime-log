import requests
from datetime import datetime

with open('key.txt', 'r') as f:
    apiKey = f.read()

url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}". \
    format(key = apiKey, steamid = "76561198024958891")

r = requests.get(url)
response = r.json()

target_game_ids = [304930]

for game in response['response']['games']:
    if game['appid'] in target_game_ids:
        print(game['playtime_forever'])

now = datetime.now()
print(str(now.date()) + ', ' + str(now.time()) + '\n')
