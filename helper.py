import requests
import json
from datetime import date

def getTable():
  url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

  querystring = {"Category":"soccer","Ccd":"turkey","Scd":"super-lig"}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "livescore6.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)  


  json_data = json.loads(response.text)

  res = []
  
  for team in json_data["Stages"][0]["LeagueTable"]["L"][0]["Tables"][0]["team"]:
      res.append([str(team["rnk"])+".",team["Tnm"],str(team["pld"]),str(team["win"]),str(team["drw"]),str(team["lst"]),str(team["gf"]),str(team["ga"]),str(team["gd"]),str(team["pts"])])
  return res


def thumbnail(team_name):

  url = "https://api-football-beta.p.rapidapi.com/teams"

  querystring = {"country":"turkey"}

  headers = {
    'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
    'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  for team in json_data["response"]:
    if team_name == team["team"]["name"]:
      return team["team"]["logo"]

def getFixture(team):
  url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

  querystring = {"Category":"soccer","Ccd":"turkey","Scd":"super-lig"}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "livescore6.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)  

  json_data = json.loads(response.text)

  res = []
  for event in json_data["Stages"][0]["Events"]:
    if event["T1"][0]["Nm"] == team:
      match_date = str(event["Esd"])
      match_date = match_date[6:8] +"."+ match_date[4:6] +"."+ match_date[0:4]
      if "Tr1" in event:
        res.append([match_date,event["T1"][0]["Nm"],event["Tr1"],event["T2"][0]["Nm"],event["Tr2"]])
      else:
        res.append([match_date,event["T1"][0]["Nm"],event["T2"][0]["Nm"]])
    elif event["T2"][0]["Nm"] == team:
      match_date = str(event["Esd"])
      match_date = match_date[6:8] +"."+ match_date[4:6] +"."+ match_date[0:4]

      if "Tr1" in event:
        res.append([match_date,event["T1"][0]["Nm"],event["Tr1"],event["T2"][0]["Nm"],event["Tr2"]])
      else:
        res.append([match_date,event["T1"][0]["Nm"],event["T2"][0]["Nm"]])
  return res

def getTeamID(team):
  url = "https://api-football-beta.p.rapidapi.com/teams"

  querystring = {"name":team,"league":"203","season":"2021"}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  return json_data["response"][0]["team"]["id"]

def getFixtureSpecs(team_id):
  url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

  querystring = {"season":"2021","team":str(team_id)}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  today = str(date.today())

  specs = {}

  for match in json_data["response"]:
    match_date = match["fixture"]["date"][:10]
    if match_date == today:
      fix_id = match["fixture"]["id"]
      leauge = match["league"]["name"]
      ven = match["fixture"]["venue"]["name"]
      match_time = str(int(match["fixture"]["date"][11:13])+3) + match["fixture"]["date"][13:16]
      home_team = match["teams"]["home"]["name"]
      away_team = match["teams"]["away"]["name"]
      specs["fix_id"]=fix_id
      specs["leauge"]=leauge
      specs["ven"]=ven
      specs["match_time"]=match_time
      specs["home_team"]=home_team
      specs["away_team"]=away_team

  return specs

def getLineup(team):

  specs = getFixtureSpecs(getTeamID(team))

  if specs == {}:
    return []
  
  url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups"

  querystring = {"fixture":str(specs["fix_id"])}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  if len(json_data["response"]) == 0:
    return [0]

  for t in json_data["response"]:
    if t["team"]["name"] == team:
      form = t["formation"]
      ff = form.split("-")
      ff = [1]+[int(i) for i in ff]

      lineup = [[] for y in range(len(ff))]
      index = 0
      for t in json_data["response"]:
        if t["team"]["name"] == team:
            form = t["formation"]
            ff = form.split("-")
            ff = [1]+[int(i) for i in ff]

            lineup = [[] for y in range(len(ff))]
            index = 0
            for r in range(len(lineup)):
                for s in range(ff[r]):
                    if t["startXI"][index]["player"]["pos"] == "G":
                        nam = t["startXI"][index]["player"]["name"].split(" ")
                        nam = str(t["startXI"][index]["player"]["number"]) + ". " + str(nam[0][0]) + "." + nam[-1] + " (G)"
                        lineup[r].append(nam)
                    else:
                        nam = t["startXI"][index]["player"]["name"].split(" ")
                        nam = str(t["startXI"][index]["player"]["number"]) + ". " + str(nam[0][0]) + "." + nam[-1]
                        lineup[r].append(nam)
                    index += 1

            lineup.append([])

            for pla in t["substitutes"]:
                if pla["player"]["pos"] == "G":
                    h = pla["player"]["name"].split(" ")
                    h = str(pla["player"]["number"]) + ". " + str(h[0][0]) + "." + h[-1] + " (G)"
                    lineup[-1].append(h)
                else:
                    h = pla["player"]["name"].split(" ")
                    h = str(pla["player"]["number"]) + ". " + str(h[0][0]) + "." + h[-1]
                    lineup[-1].append(h)
            
            lineup.append([t["coach"]["name"],form])

            return lineup


def getCurrentRound():

  url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

  querystring = {"league":"203","season":"2021","current":"true"}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  return json_data["response"][0]

def getWeek():

  url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

  querystring = {"league":"203","season":"2021","round":getCurrentRound()}

  headers = {
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a",
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)

  data = {
    "week":getCurrentRound()[-1],
    "matches":[]
    }
  for item in json_data["response"]:

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/events"

    querystring = {"fixture":str(item["fixture"]["id"]),"type":"Goal"}

    headers = {
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
      'x-rapidapi-key': "019c2f19d1mshe3bf2a679896616p116eaejsn4d88f8edc40a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    goals = json.loads(response.text)["response"]

    match = {}
    match_date = item["fixture"]["date"][0:10]
    match["match_date"] = match_date
    match_time = item["fixture"]["date"][11:16]

    hour = str(int(match_time[:2])+3)
    match_time = hour + match_time[2:]

    match["match_time"] = match_time

    home_team = item["teams"]["home"]["name"]
    away_team = item["teams"]["away"]["name"]

    status = item["fixture"]["status"]["short"]

    match["status"] = status
    match["home"] = {
      "team":home_team,
      "goal":item["goals"]["home"],
      "scorers": []
      }
    match["away"] = {
      "team":away_team,
      "goal":item["goals"]["away"],
      "scorers": []
      }
    
    for goal in goals:
      g = str(goal["time"]["elapsed"]) + "' " + goal["player"]["name"]

      if goal["detail"] == "Penalty":
        g += " (P)"

      if goal["team"]["name"] == home_team:
        match["home"]["scorers"].append(g)
        print(match["home"]["scorers"][-1])
      else:
        match["away"]["scorers"].append(g)
        print(match["home"]["scorers"][-1])



    data["matches"].append(match)
  
  return data






