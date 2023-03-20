import datetime
import json

import requests

from bs4 import BeautifulSoup


from Parser import Parser
from model.Game import Game
from model.events.Card import Card
from model.events.Substitution import Substitution
from model.events.Goal import Goal

import pytz


def thumbnail(team_name):

  url = "https://api-football-beta.p.rapidapi.com/teams"

  querystring = {"country":"turkey"}

  response = Parser(url, querystring).get_data()

  for team in response:
    if team_name == team["team"]["name"]:
      return team["team"]["logo"]

def getTeamIdByName(name):
    response = Parser('https://api-football-v1.p.rapidapi.com/v3/teams', {
        'name': name
    }).get_data()

    return response[0]['team']['id']

def getHighlightVideo(team_name):

  url_prefix = 'https://beinsports.com.tr'

  response = requests.request("GET",f'https://beinsports.com.tr/takim/{team_name}/videolar')

  # turn response into a beautiful soup object

  soup = BeautifulSoup(response.text, 'html.parser')

  # find all the divs with the class 'video-list-item'

  video = soup.find_all('div', class_='media-list-item')[0]

  # get href

  href = video.find('a')['href']

  response = requests.request("GET", url_prefix + href)

  soup = BeautifulSoup(response.text, 'html.parser')

  script_tag = soup.find_all('script')[1]

  # get content url from script tag

  contents = script_tag.contents[0]

  # convert to json


  contents = json.loads(contents)

  # get video url

  video_url = contents['contentUrl']

  return video_url

def getEventList(last_game):

  result = [
        '{:>30} {} - {} {:<30}\n'.format(
            last_game.home_team,
            str(last_game.home_score),
            str(last_game.away_score),
            last_game.away_team
        )
    ]

    # utf-8 yellow

  for event in last_game.events:
      if event.team == last_game.home_team:
          if isinstance(event, Goal) and event.own_goal:
              result.append('{:>8}{} - {}'.format(
                  '\u26BD ' + event.scorer + ' (OG)',
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

          elif isinstance(event, Goal) and event.penalty:
              result.append('{:>8}{} - {}'.format(
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
                  '\u26BD ' + event.scorer + ' (P)',
              ))

          elif isinstance(event, Goal):
              result.append('{:>8}{} - {}'.format(
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
                  '\u26BD ' + event.scorer)
              )

              if event.assist:
                  result.append('          {}'.format(
                      '(' + event.assist + ')' if event.assist else '')
                  )

          elif isinstance(event, Card):
              result.append('{:>8}{} - {}'.format(
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
                  '\U0001F7E8 ' + event.player if event.card_type == 'Yellow Card' else '\U0001F534 ' + event.player
              ))

          elif isinstance(event, Substitution):
              result.append('{:>8}{} - {}'.format(
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
                   event.player_in + ' \u21B0'
              ))

              result.append('          {}'.format(
                  '\u21B3 ' + event.player_out
              ))




      else:
          if isinstance(event, Goal) and event.own_goal:
              result.append('{:>55} - {}{}'.format(
                  '\u26BD ' + event.scorer + ' (OG)',
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

          elif isinstance(event, Goal) and event.penalty:
              result.append('{:>55} - {}{}'.format(
                  '\u26BD ' + event.scorer + ' (P)',
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

          elif isinstance(event, Goal):
              result.append('{:>50} - {}{}'.format(
                  '\u26BD ' + event.scorer,
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

              if event.assist:
                  result.append('{:>53}'.format(
                      '(' + event.assist + ')' if event.assist else '')
                  )

          elif isinstance(event, Card):
              result.append('{:>51} - {}{}'.format(
                  '\U0001F7E8 ' + event.player if event.card_type == 'Yellow Card' else '\U0001F7E5 ' + event.player,
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

          elif isinstance(event, Substitution):
              result.append('{:>50} - {}{}'.format(
                  event.player_in + ' \u21B0',
                  event.minute,
                  '+' + str(event.extra) if event.extra else '',
              ))

              result.append('{:>50}'.format(
                  '\u21B3 ' + event.player_out
              ))

  return result

def getCurrentRound():

    response = Parser('https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds', {
        'league': '203',
        'season': '2022',
        'current': 'true'
    }).get_data()

    return response[-1]

def getMatchesByRound(round):

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
            match['fixture']['id'],
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

def printWeek(matches):
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


