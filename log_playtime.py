import requests
from datetime import datetime

id_to_name = {43110: "name_of_game",
              265630: "other_name_of_game"}
delimiter = ', '


def save_local(game_object):
    """
    Saves playtime to a local file.
    :param game_object:
    """
    app_id = game_object['appid']
    filename = "out/{} {}.txt".format(app_id, id_to_name[app_id])
    now = datetime.now()

    with open(filename, "w+") as f:
        f.write("{date}{_}{time}{_}{appid}{_}{playtime}\n".format(
            _ = delimiter,
            date = now.date(),
            time = now.time(),
            appid = app_id,
            playtime = game_object['playtime_forever']
        ))

with open('steam_api_key.txt', 'r') as f:
    api_key = f.read()

url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}". \
    format(api_key = api_key, steam_id = "76561198024958891")  # replace with your steam id

r = requests.get(url)
response = r.json()

for game in response['response']['games']:
    if game['appid'] in id_to_name.keys():
        save_local(game)
