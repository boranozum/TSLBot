import discord
import os
import helper
from keepalive import keep_alive
from discord.ext import commands
from datetime import date

client = commands.Bot(command_prefix = "$")

async def on_ready(self):
    print('Logged on as', self.user)

@client.command()
async def puan(ctx):  
  DATASET = helper.getTable()
  s = [' Sıra       Takım        O   G   B   M   A   Y  Avg. P']
  for data in DATASET:
      s.append(data[0].center(5,' ')+data[1].center(19,' ')+data[2].center(4, ' ')+data[3].center(4, ' ')+data[4].center(4, ' ')+data[5].center(4, ' ')+data[6].center(4, ' ')+data[7].center(4, ' ')+data[8].center(4, ' ')+data[9].center(4, ' '))
        # Joining up scores into a line
  d = '```'+'\n'.join(s) + '```'
    # Joining all lines together! 
  embed = discord.Embed(title = 'Süper Lig - Puan Durumu', description = d, color=discord.Colour.random())
  await ctx.send(embed=embed)

@client.command()
async def fix(ctx,arg):
  DATASET = helper.getFixture(arg)

  s = ["   Tarih                      Maç"]

  for data in DATASET:
    if len(data)==3:
      s.append(data[0].center(12," ")+(data[1] + " - " +data[2]).center(40," "))
    else:
      s.append(data[0].center(12," ")+(data[1] + "{} - {}".format(data[2],data[4]) +data[3]).center(40," "))

  d = '```'+'\n'.join(s) + '```'

  embed = discord.Embed(title = "{} - Fikstür".format(arg), description=d,color=discord.Colour.random())
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
