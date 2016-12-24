# Steam playtime logger

Logs playtime of Steam games to a local text file and/or to a Google Sheets spreadsheet.

## Usage

1. Get a Steam API key at http://steamcommunity.com/dev/apikey and put it in [`steamid`](log_playtime.py#L79)
1. If you want to save logs to Google Sheets:
   1. Follow Google's [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
   1. Save the various JSON files in this directory
   1. Create a new spreadsheet on Google Sheets and put the ID in [`spreadsheet_id`](google_sheets.py#L107)
1. Create a folder called `out` in this directory, or change [`path`](log_playtime.py#L63) to change where files are written
1. Find the appIDs of the games you want to log, and put them in [`appids_to_log`](log_playtime.py#L80)
1. Go [here](log_playtime.py#L84-L85) and comment or uncomment the functions to write the logs to a local text file or to Google Sheets
1. Run `log_playtime.py`
1. Results:
   * By default, the filenames of the local logs are formatted like `[appID] gameName.txt`, eg. `[440] Team Fortress 2.txt`. The contents are comma-seperated values, eg.
   ```
    "Date", "Time", "Playtime (minutes)"
    "2016-12-23", "22:16:18.869231", "525"
   ```
   * Google Sheets output is similar.



## Background

The target application was VR arcades, where game developers want to know how much their game is being played.

Steam shows playtimes in the web interface, so you could scrape the data from the webpage. Here's the display at
`http://steamcommunity.com/profiles/xxxxxxxxxxxxxxxxx/games/?tab=all`:

<p align="center" style="text-align: center">
<img src="time_on_record.png?raw=true" alt="Steam playtime on record">
</p>

But we can bypass this step by using the [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API). You can see what output from the API looks like in [`steam_api_response.txt`](steam_api_response.txt).
