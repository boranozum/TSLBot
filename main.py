import discord
import os
import helper
from keepalive import keep_alive
from discord.ext import commands
from datetime import date
from League import League
from utils import getTeamIdByName, printWeek

client = commands.Bot(command_prefix = "$")
league = League(league_id=203)

async def on_ready(self):
    print('Logged on as', self.user)

@client.command(name='standings', help='Get the league standings')
async def standings(ctx):  
  league.setStandings()
  embed = discord.Embed(title = 'Süper Lig - Puan Durumu', description = league.printStandings(), color=discord.Colour.random())
  await ctx.send(embed=embed)

@client.command()
async def fix(ctx,arg):

  team_id = getTeamIdByName(arg)

  team = league.teams[team_id]
  team.setMatches()

  embed = discord.Embed(title = "{} - Fikstür".format(arg), description=team.printMatches(),color=discord.Colour.random())
  embed.set_thumbnail(url=helper.thumbnail(arg))

  await ctx.send(embed=embed)

@client.command()
async def onbir(ctx,arg):
  DATASET = helper.getLineup(arg)
  if DATASET == []:
    message = "{} takımının bugün maçı yok!".format(arg)
    await ctx.send(message)
  elif DATASET[0] == 0:
    message = "11'ler henüz açıklanmadı!"
    await ctx.send(message)
  else:
    specs = helper.getFixtureSpecs(helper.getTeamID(arg))
    if specs["home_team"] == arg:
      opp = specs["away_team"]
    else:
      opp = specs["home_team"]
    s = []
    for data in DATASET[:-2]:
      if(len(data)==1):
        f = data[0]
        s.append(f.center(60," ")+ "\n\n\n")
      else:
        m = ""
        for player in data:
          m += player.center(12," ") + " "
        m = m.center(60, " ") + "\n\n\n"
        s.append(m)
    
    d = '```'+'\n'.join(s) + '```'

    embed = discord.Embed(title = "{} - İlk 11 (vs. {})".format(arg,opp), description=d,color=discord.Colour.random())
    #embed.set_thumbnail(url=thumbnail(arg))
    subs= ""
    for pla in DATASET[-2]:
      subs += ", "+pla

    subs = subs[2:]

    embed.set_footer(text="Yedekler: {}\n\nDiziliş: {}          Teknik Direktör: {}          Maç Saati: {}          Stadyum: {}".format(subs,DATASET[-1][1],DATASET[-1][0],specs["match_time"],specs["ven"]))

    await ctx.send(embed=embed)


@client.command()
async def week(ctx):

  week = printWeek()
    
  embed = discord.Embed(color=discord.Colour.random(),description = week)

  embed.set_footer(text= "* : Live")
  await ctx.send(embed=embed)



keep_alive()

client.run(os.getenv('TOKEN'))
