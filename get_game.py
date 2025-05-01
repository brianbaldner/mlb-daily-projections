import json
from functions import session
from analysis import run
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys

date  = (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d")

if len(sys.argv) > 1 and sys.argv[1] != "":
    date = sys.argv[1]

greq = session.get(f"https://baseballsavant.mlb.com/schedule?date={date}")
day = json.loads(greq.text)

result = pd.DataFrame()

for game in day["schedule"]["dates"][0]["games"]:
    print(f"Starting {game["teams"]["away"]["team"]["clubName"]} @ {game["teams"]["home"]["team"]["clubName"]}")
    res = session.get(f"https://baseballsavant.mlb.com/preview?game_pk={game["gamePk"]}&game_date={game["officialDate"]}")
    home_abbr = game["teams"]["home"]["team"]["abbreviation"]
    away_abbr = game["teams"]["away"]["team"]["abbreviation"]
    data = res.text

    start_index = data.find("var teams = ")

    end_index = data.find(";", start_index + 12)

    data = data[start_index + 12:end_index]

    parsed = json.loads(data)

    home_hitters = []

    for i in parsed["home"]["roster"]["hitters"]:
        try:
            home_hitters.append(str(i["player_id"]))
        except:
            try:
                print(f"Error with player {i["person"]["fullName"]}")
            except:
                print("Error with random player")

    away_hitters = []

    for i in parsed["away"]["roster"]["hitters"]:
        try:
            away_hitters.append(str(i["player_id"]))
        except:
            try:
                print(f"Error with player {i["person"]["fullName"]}")
            except:
                print("Error with random player")

    home_prob = ""
    home_prob_hand = ""

    for i in parsed["home"]["roster"]["pitchers"]:
        try:
            if i["isPlaying"]:
                home_prob = str(i["player_id"])
                home_prob_hand = str(i["pitch_hand"])
                break
        except:
            continue

    away_prob = ""
    away_prob_hand = ""

    for i in parsed["away"]["roster"]["pitchers"]:
        try:
            if i["isPlaying"]:
                away_prob = str(i["player_id"])
                away_prob_hand = str(i["pitch_hand"])
                break
        except:
            continue
    try:
        if(away_prob != ""):
            result = pd.concat([result, run(home_hitters, away_prob, home_abbr, away_prob_hand)], ignore_index=True)
    except Exception as e:
        print(f"Error with {game["teams"]["home"]["team"]["clubName"]} batters\n{repr(e)}")

    try:
        if(home_prob != ""):
            result = pd.concat([result, run(away_hitters, home_prob, away_abbr, home_prob_hand)], ignore_index=True)
    except Exception as e:
        print(f"Error with {game["teams"]["away"]["team"]["clubName"]} batters\n{repr(e)}")
    print(result)

    result.to_csv("result.csv", encoding='utf-16')

result["Net Matchup vs Avg (hits)"] = result["H / 5ab"] - result["AVG H / 5ab"]
result["Net Matchup vs Avg (bases)"] = result["B / 5ab"] - result["AVG B / 5ab"]
result.to_csv("result.csv", encoding='utf-16')

result = result[result["PA"] > 50]

pot = px.scatter(result, x="H / 5ab", y="B / 5ab", color='PA', hover_data={"Name": True, "Net Matchup vs Avg (hits)" : True, "Net Matchup vs Avg (bases)" : True, "Opposing Pitcher" : True,}, title=f"Matchup Analysis for {date}")
pot.write_html("index.html", include_plotlyjs="cdn")