import discord
import os
import helper
from keepalive import keep_alive
from discord.ext import commands
from datetime import date
from Leauge import League
from Leauge import getTeamIdByName

client = commands.Bot(command_prefix = "$")
league = League(league_id=203)

commands = {
    'help': 'help',
    'standings': 'standings',
    'fixtures': 'fixtures',
}


async def handle_help_command(message):
  help_message = "Here are the available commands:\n\n"
  for command, description in commands.items():
      help_message += f"`{command}`: {description}\n"
  await message.channel.send(help_message)

async def handle_command(message):
    # Parse the message to get the command and any arguments
    command, *args = message.content[1:].split()

    # Check if the command is "help" and call the handle_help_command function if it is
    if command == "help":
        await handle_help_command(message)

@client.event
async def on_message(message):
  if message.content.startswith("$"): 
      await handle_command(message)

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
async def hafta(ctx):
  DATASET = helper.getWeek()

  dates = {}
  for data in DATASET["matches"]:
    if data["status"] == "NS":
      if data["match_date"] not in dates:
        dates[data["match_date"]] = [data["match_time"] +data["home"]["team"]+" - "+data["away"]["team"]]
      else:
        dates[data["match_date"]].append(data["match_time"] +data["home"]["team"]+" - "+data["away"]["team"])
    elif data["status"] != "FT":
      if data["match_date"] not in dates:
        dates[data["match_date"]] = [data["match_time"] +data["home"]["team"]+ " " +str(data["home"]["goal"])  +" -* " +str(data["away"]["goal"])+ " " +data["away"]["team"]] 
      else:
        dates[data["match_date"]].append(data["match_time"] +data["home"]["team"]+ " " +str(data["home"]["goal"]) + " -* " +str(data["away"]["goal"])+ " " +data["away"]["team"])
      
    else:
      if data["match_date"] not in dates:
        dates[data["match_date"]] = [data["match_time"] +data["home"]["team"]+ " " +str(data["home"]["goal"]) + " - " +str(data["away"]["goal"])+ " " +data["away"]["team"]]
      else:
        dates[data["match_date"]].append(data["match_time"] +data["home"]["team"]+ " " +str(data["home"]["goal"]) + " - " +str(data["away"]["goal"])+ " " +data["away"]["team"])

    
  dates = dict(sorted(dates.items()))
  
  s = []

  

  for day in dates:
    y = date(int(day[:4]),int(day[5:7]),int(day[8:10]))
    if y.strftime("%A") == "Monday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Pazartesi"
    if y.strftime("%A") == "Tuesday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Salı"
    if y.strftime("%A") == "Wednesday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Çarşamba"
    if y.strftime("%A") == "Thursday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Perşembe"
    if y.strftime("%A") == "Friday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Cuma"
    if y.strftime("%A") == "Saturday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Cumartesi"
    if y.strftime("%A") == "Sunday":
      dd = day[8:10] + "." + day[5:7] + "." + day[:4] + " - " + "Pazar"
    s.append("  "+dd+"\n")

    for match in sorted(dates[day]):
      s.append("     " + match[:5] + match[5:].center(50," "))

    s.append("\n")
    
  d = '```'+'\n'.join(s) + '```'
    
  embed = discord.Embed(title = "Süper Lig {}. Hafta".format(DATASET["week"]),color=discord.Colour.random(),description = d)

  embed.set_footer(text= "-* : Maç devam ediyor")
  await ctx.send(embed=embed)



keep_alive()

client.run(os.getenv('TOKEN'))
