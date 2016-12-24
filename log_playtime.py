import requests
from google_sheets import save_to_sheets


def get_owned_games(steamid, appids):
    """
    Queries the Steam API for info about the specified games owned by the specified user.
    Look at steam_api_response.txt to see how the response is structured.

    :param steamid: the SteamID of the user who owns the games
    :type steamid: int
    :param appids: IDs of the Steam apps to get info about
    :type appids: list
    :return: a dictionary (JSON) containing game information
    :rtype: dict
    """

    # Get yer API key at http://steamcommunity.com/dev/apikey
    with open('steam_api_key.txt', 'r') as f:
        api_key = f.read()

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    params = {
        "key": api_key,
        "steamid": steamid,
        "include_played_free_games": 1,
        "include_appinfo": 1,
    }

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    # Valve's documentation for GetOwnedGames says appids_filter "cannot be passed as a URL parameter" and you must use
    # "a new style of WebAPI which we [Steam] refer to as 'Services'".
    #
    # So, allegedly, appids_filter must be passed as a JSON parameter: input_json={appids_filter: [440, 500, 550]}.
    # But this doesn't work. Passing appids_filter as a normal parameter doesn't work either.
    #
    # https://wiki.teamfortress.com/wiki/WebAPI/GetOwnedGames#Method-specific_parameters
    # The Team Fortress Wiki also documents Steam's web API. About the appids_filter parameter, it says
    # "This is an array and should be passed like appids_filter[0]=440&appids_filter[1]=570"
    # with no mention of Services or JSON. This is the only way that works, so that's what I do here.
    for index, appid in enumerate(appids):
        key = "appids_filter[{}]".format(index)
        params[key] = appid

    r = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/", params=params)
    r.raise_for_status()
    return r.json()


def save_locally(game_obj):
    """
    Writes playtime for one game to a text file.

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


def main():
    """

    """
    steamid = 76561198024958891  # your steamID here
    appids_to_log = [43110, 265630]  # customize appIDs here

    api_response = get_owned_games(steamid, appids_to_log)
    for game in api_response['response']['games']:
        save_locally(game)
        # save_to_sheets(game)


main()
