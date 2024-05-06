import requests
import requests_cache
import json

def getPlayerID(playerName):
    link = "https://trackmania.io/api/players/find?search={}".format(playerName)
    headers = {
        'User-Agent': 'Displays number of players in COTD using a Twitch command. For questions about this project, contact me on Discord: Johnnycyan#0001',
    }
    requests_cache.install_cache('cotd_cache', backend='sqlite', expire_after=3600)
    page = requests.get(link, headers=headers).text
    jsonLoading = json.loads(page)
    playerID = jsonLoading[0]["player"]["id"]
    return playerID

def getFormattedName(playerName):
    link = "https://trackmania.io/api/players/find?search={}".format(playerName)
    headers = {
        'User-Agent': 'Displays number of players in COTD using a Twitch command. For questions about this project, contact me on Discord: Johnnycyan#0001',
    }
    requests_cache.install_cache('cotd_cache', backend='sqlite', expire_after=3600)
    page = requests.get(link, headers=headers).text
    jsonLoading = json.loads(page)
    formattedName = jsonLoading[0]["player"]["name"]
    return formattedName