import datetime
import pytz

from Parser import Parser
from League import Game


def getTeamIdByName(name):
  response = Parser('https://api-football-v1.p.rapidapi.com/v3/teams', {
      'name': name
  }).get_data()

  return response[0]['team']['id']

def getCurrentRound():

    response = Parser('https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds', {
        'league': '203',
        'season': '2022',
        'current': 'true'
    }).get_data()

    return response[0]

def getMatchesByRound():

  round = getCurrentRound()

  response = Parser('https://api-football-v1.p.rapidapi.com/v3/fixtures', {
      'league': '203',
      'season': '2022',
      'round': round
  }).get_data()

  matches = []

  for match in response:
    status = match['fixture']['status']['short']

    if status == 'CANC':
      continue
      
    timestamp = match['fixture']['timestamp']
    # get the date, time and day of the week from the timestamp
    date = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Istanbul')).strftime('%d-%m-%Y')
    time = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Istanbul')).strftime('%H:%M')
    day = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Istanbul')).strftime('%A')
    elapsed = match['fixture']['status']['elapsed']

    game = Game(
        match['teams']['home']['name'],
        match['teams']['away']['name'],
        match['goals']['home'],
        match['goals']['away'],
        status=status,
        date=date,
        time=time,
        day=day,
        elapsed=elapsed)

    matches.append(game)

  # sort the matches by date then time
  matches.sort(key=lambda x: (x.date, x.time))
  return matches

def printWeek():
  matches = getMatchesByRound()
  starting_date = matches[0].date
  week = [matches[0].date + ', ' + matches[0].day + '\n']

  for match in matches:
    if starting_date != match.date:
      starting_date = match.date
      week[-1] += '\n'
      week.append(match.date + ', ' + match.day + '\n')

    week.append(match.__repr__())

  week = '```' + '\n'.join(week) + '```'
  return week


