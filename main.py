import discord
import os
from keepalive import keep_alive
from discord.ext import commands
from datetime import date

import requests

from bs4 import BeautifulSoup

import json

from model.League import League
from utils import getTeamIdByName, printWeek, thumbnail, getMatchesByRound, getCurrentRound, getHighlightVideo, getEventList

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
async def lastmatch(ctx, arg):

  league = League(league_id=203)
  team_id = getTeamIdByName(arg)

  team = league.teams[team_id]

  last_game = team.getLastMatch()

  last_game.set_events()

  

  video_url = getHighlightVideo(arg)

  embed = discord.Embed()
  embed.description = "```" + '\n'.join(getEventList(last_game))  + "```"
  embed.add_field(name="Highlights", value=f"[Watch now]({video_url})")

  await ctx.send(embed=embed)

keep_alive()

client.run(os.getenv('TOKEN'))
