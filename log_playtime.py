import requests
from google_sheets import save_to_sheets


def get_owned_games(steamid_, appids):
    """
    Returns dict with information about owned games.
    :param steamid_: SteamID of user
    :param appids: list of appids of the games to log time of
    :type steamid_: int
    :type appids: list
    :return: dict
    """
    with open('steam_api_key.txt', 'r') as f:
        api_key = f.read()

    appids_filter_array = ''
    for index, appid in enumerate(appids):
        appids_filter_array += '&appids_filter[{}]={}'.format(index, appid)

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&include_appinfo=1{}'. \
        format(api_key, steamid_, appids_filter_array)

    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def save_locally(game_obj):
    """
    Saves playtime for one game to a local log file.
    :param game_obj: dict (from json object) with game and playtime information
    :type game_obj: dict
    """
    from datetime import datetime
    path = 'out/{} {}.txt'.format(game_obj['appid'], game_obj['name'])
    now = datetime.now()
    with open(path, 'w+') as f:
        row = [now.date(), now.time(), game_obj['playtime_forever']]
        row = map(str, row)
        f.write(', '.join(row))


steamid = 76561198024958891  # replace with your steamID
appids_to_log = [43110, 265630]
for game in get_owned_games(steamid, appids_to_log)['response']['games']:
    # save_locally(game)
    save_to_sheets(game)
