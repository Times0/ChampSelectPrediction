import json
import os

import riotwatcher
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")  # refrsh api key : https://developer.riotgames.com/
REGION = "EUW1"

lol_watcher = riotwatcher.LolWatcher(API_KEY)

m = lol_watcher.league.masters_by_queue(REGION, "RANKED_SOLO_5x5")
gm = lol_watcher.league.grandmaster_by_queue(REGION, "RANKED_SOLO_5x5")
c = lol_watcher.league.challenger_by_queue(REGION, "RANKED_SOLO_5x5")
players_dict: dict = json.load(open("players.json", "r"))
for player in m["entries"] + gm["entries"] + c["entries"]:
    if not player["summonerName"]:
        print("No summoner name")
        continue
    if player["summonerName"] in players_dict:
        print("Already in")
        continue
    summoner = lol_watcher.summoner.by_name(REGION, player["summonerName"])
    players_dict[player["summonerName"]] = summoner["puuid"]
    json.dump(players_dict, open("players.json", "w"))

last_game_ids = []
for player_name, player_puid in players_dict.items():
    matchlist = lol_watcher.match.matchlist_by_puuid(REGION, player_puid)
    if matchlist["matches"]:
        last_game_ids.append(matchlist["matches"][0]["gameId"])

print(last_game_ids)

lol_watcher.summoner.by_name(REGION, "Times")
