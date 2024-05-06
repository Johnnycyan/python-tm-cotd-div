import requests
import requests_cache
import json
import math
import inflect
from datetime import datetime
from getPlayerID import getPlayerID
from getPlayerID import getFormattedName
from flask import Flask
from flask import request
from markupsafe import escape
import re

app = Flask(__name__)

@app.route('/div')
def application():
    try:
        try:
            playerName = request.args.get('playerName')
        except:
            return "Error: No player name was provided."
        try:
            if playerName.lower() == "maji":
                playerName = "majijej"
            elif playerName.lower() == "wirtual":
                playerName = "wirtualtm"
            elif playerName.lower() == "wirt":
                playerName = "wirtualtm"
            elif playerName.lower() == "jnic":
                playerName = "j.nic"
        except:
            return "Error: Player name is invalid."
        
        try:
            playerID = getPlayerID(playerName)
        except:
            return "Error: Player name is invalid."
        try:
            emote = request.args.get('emote')
            emote = "{} ".format(emote)
            if emote == "None ":
                emote = ""
        except:
            emote = ""
        formattedName = getFormattedName(playerName)
        link = "https://trackmania.io/api/player/{}/trophies/0".format(playerID)
        headers = {
            'User-Agent': 'Displays specified user\'s div in COTD for a Twitch command. For questions about this project, contact me on Discord: Johnnycyan#0001',
        }
        rank = 0
        div = 0
        p = inflect.engine()
        currentDateAndTime = datetime.now()
        currentHour = currentDateAndTime.hour
        with requests_cache.enabled('div_cache', backend='sqlite', expire_after=20):
            page = requests.get(link, headers=headers).text
        jsonLoading = json.loads(page)
        count = 0
        try:
            for i in jsonLoading["gains"]:
                try:
                    compType = jsonLoading["gains"][count]["achievement"]["competitionType"]
                except:
                    count += 1
                    continue
                if compType == "DailyCup":
                    try:
                        stageStep = jsonLoading["gains"][count]["achievement"]["competitionStageStep"]
                    except:
                        count += 1
                        continue
                    try:
                        if stageStep == "Ranking":
                            div = int((jsonLoading["gains"][count]["details"]["rank"]))
                            try:
                                date = jsonLoading["gains"][count]["achievement"]["competitionName"]
                                date = re.search('\d\d\d\d-\d\d-\d\d', date).group()[5:10]
                            except:
                                return "Error: Player has not played recently enough."
                            break
                        else:
                            count += 1
                            continue
                    except:
                        count += 1
                        continue
                else:
                    count += 1
                    continue
        except:
            return "Error: Player has not played recently enough."
        try:
            if stageStep != "Ranking":
                link = "https://trackmania.io/api/player/{}/trophies/1".format(playerID)
                headers = {
                    'User-Agent': 'Displays specified user\'s div in COTD for a Twitch command. For questions about this project, contact me on Discord: Johnnycyan#0001',
                }
                rank = 0
                div = 0
                if currentHour >= 13 and currentHour < 15:
                    page = requests.get(link, headers=headers, expire_after=60).text
                else:
                    page = requests.get(link, headers=headers).text
                jsonLoading = json.loads(page)
                count = 0
                for i in jsonLoading["gains"]:
                    try:
                        compType = jsonLoading["gains"][count]["achievement"]["competitionType"]
                    except:
                        count += 1
                        continue
                    if compType == "DailyCup":
                        try:
                            stageStep = jsonLoading["gains"][count]["achievement"]["competitionStageStep"]
                        except:
                            count += 1
                            continue
                        if stageStep == "Ranking":
                            div = int((jsonLoading["gains"][count]["details"]["rank"]))
                            try:
                                date = jsonLoading["gains"][count]["achievement"]["competitionName"]
                                date = re.search('\d\d\d\d-\d\d-\d\d', date).group()[5:10]
                            except:
                                return "Error: Player has not played recently enough."
                            break
                        else:
                            count += 1
                            continue
                    else:
                        count += 1
                        continue
        except:
            return "Error: Player has not played recently enough."
        try:
            if stageStep != "Ranking":
                return "Error: Player has not played recently enough."
        except:
            return "Error: Player has not played recently enough."

        div = int(math.ceil(div / 64))

        if playerName.lower() == "majijej":
            formattedName = "Maji"
        elif playerName.lower() == "wirtualtm":
            formattedName = "Wirtual"

        try:
            return f"{escape(formattedName)} is in div {escape(div)} {escape(emote)}| {escape(date)}"
        except:
            return "Error: Player has not played recently enough."
    except:
        return "Error: An unknown error has occurred."

if __name__ == "__main__":
    app.run()