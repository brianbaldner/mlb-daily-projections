import time
import numpy as np
import pandas as pd
import io
import requests
from functions import pitcher_req, batter_request
import warnings
warnings.simplefilter('ignore', FutureWarning)

oppo_hand = {
    "R": "L",
    "L": "R"
}

names = pd.read_csv("names.csv", index_col="player_id", encoding="utf-8")
pitch_types = {
    "FF": "Four Seamer",
    "SI": "Sinker",
    "FC": "Cutter",
    "CH": "Changeup",
    "FS": "Split-finger",
    "FO": "Forkball",
    "SC": "Screwball",
    "CU": "Curveball",
    "KC": "Knuckle Curve",
    "CS": "Slow Curve",
    "SL": "Slider",
    "ST": "Sweeper",
    "SV": "Slurve",
    "KN": "Knuckleball",
    "EP": "Eephus",
    "FA": "Other",
    "IN": "Intentional Ball",
    "PO": "Pitchout"
}

def run(hitters, pitcher, team, phand) -> pd.DataFrame:
    pitcher = pitcher_req(pitcher, ["2025"])
    pname = pitcher['player_name'].iloc[0]
    pitcher["pitch_type"] = pitcher["pitch_type"].apply(lambda x: pitch_types[x])
    pitcher.index = pitcher["pitch_type"]

    result = pd.DataFrame()
    for playerid in hitters:
        time.sleep(0.5)
        hitter = batter_request(playerid, ["2025", "2024"], phand)

        edited_table = hitter.loc[:, ["pitches", "pitch_type", "hits", "singles", "doubles", "triples", "hrs", "pa"]].fillna(0)
        edited_table["pitch_type"] = edited_table["pitch_type"].apply(lambda x: pitch_types[x])
        edited_table = edited_table.groupby("pitch_type").aggregate(sum)

        edited_table["hit/pitch"] = edited_table["hits"] / edited_table["pitches"]
        edited_table["bases"] = edited_table["singles"] + edited_table["doubles"] * 2 + edited_table["triples"]*3 + edited_table["hrs"] * 4
        edited_table["bases/pitch"] = edited_table["bases"] / edited_table["pitches"]
        # edited_table = edited_table.sort_values("bases/pitch", ascending=False)

        average_pa = edited_table["pitches"].sum() / edited_table["pa"].sum()
        avghp = edited_table["hits"].sum() / edited_table["pitches"].sum() * average_pa * 5
        avgbp = edited_table["bases"].sum() / edited_table["pitches"].sum() * average_pa * 5

        batter_hand = names.loc[int(playerid)]["bat_hand"]
        if batter_hand == "S":
            batter_hand = oppo_hand[phand]
        
        pitches = pitcher[pitcher["batter_hand"] == batter_hand]["pitches"]
        perc = pitches / pitches.sum()
        perc = perc * average_pa * 5
        hp = perc * edited_table["hit/pitch"]
        bp = perc * edited_table["bases/pitch"]
        print(f"{names.loc[int(playerid)]["player_name"]} will get {hp.sum()} hits and {bp.sum()} bases per 5 ab")
        result = pd.concat([result, pd.DataFrame([{
            "Player ID": playerid,
            "Name": names.loc[int(playerid)]["player_name"],
            "Team": team,
            "Opposing Pitcher": pname,
            "H / 5ab": hp.sum(),
            "B / 5ab": bp.sum(),
            "AVG H / 5ab": avghp,
            "AVG B / 5ab": avgbp,
            "PA": edited_table["pa"].sum()
        }])])
    return result