import discord
import os
from keepalive import keep_alive
from discord.ext import commands
from datetime import date

import requests

from bs4 import BeautifulSoup

import json

from model.League import League
from utils import getTeamIdByName, printWeek, thumbnail, getMatchesByRound, getCurrentRound

client = commands.Bot(command_prefix="$")


async def on_ready(self):
    print('Logged on as', self.user)


@client.command(name='standings', help='Get the league standings')
async def standings(ctx):
    league = League(league_id=203)
    league.setStandings()
    embed = discord.Embed(title='Süper Lig - Puan Durumu', description=league.printStandings(),
                          color=discord.Colour.random())
    await ctx.send(embed=embed)


@client.command()
async def fix(ctx, arg):
    league = League(league_id=203)
    team_id = getTeamIdByName(arg)

    team = league.teams[team_id]
    team.setMatches()

    embed = discord.Embed(title="{} - Fikstür".format(arg), description=team.printMatches(),
                          color=discord.Colour.random())
    # embed.set_thumbnail(url=thumbnail(arg))

    await ctx.send(embed=embed)


@client.command()
async def week(ctx):

    matches_of_the_week = getMatchesByRound(getCurrentRound())

    embed = discord.Embed(color=discord.Colour.random(), description=printWeek(matches_of_the_week))

    embed.set_footer(text="* : Live")
    await ctx.send(embed=embed)

@client.command()
async def highlight(ctx, arg):

  url_prefix = 'https://beinsports.com.tr'

  response = requests.request("GET",f'https://beinsports.com.tr/takim/{arg}/videolar')

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

  embed = discord.Embed()
  embed.title = "Match Highlights"
  embed.description = "Check out the highlights from the last match!"
  embed.set_footer(text="Provided by Example.com")
  embed.add_field(name="Video", value=f"[Watch now]({video_url})")

  await ctx.send(embed=embed)

keep_alive()

client.run(os.getenv('TOKEN'))
