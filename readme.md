# Steam playtime logger

Logs playtime of Steam games to a local text file and/or to a Google Sheets spreadsheet.

Steam shows playtimes in the web interface, so you could scrape the data from the webpage. Here's the display at
`http://steamcommunity.com/profiles/xxxxxxxxxxxxxxxxx/games/?tab=all`:

<p align="center" style="text-align: center">
<img src="timeOnRecord.png?raw=true" alt="Steam playtime on record">
</p>

Buy we can bypass this step by using the [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API). You can see example JSON output at [`steam_api_response.txt`](steam_api_response.txt).

Using the Google Sheets API is more complicated, but you can follow their [quickstart guide](https://developers.google.com/sheets/api/quickstart/python).

The target application was VR arcades, where game developers want to know how much their game is being played.