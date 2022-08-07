import discord 
from discord.ext import commands
import os
import requests
import json
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ';', help_command=None)
apikey = os.environ['apikey']

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Help', 
    description = 'A list of commands', 
    color = discord.Color.blue(),
  )
  embed.set_footer(text='')
  embed.set_author(name='Weather Bot',icon_url='https://cdn.discordapp.com/attachments/909115750218862592/935301531601875014/weather02-512.png')
  embed.add_field(name='General Commands', value=';help - A list of helpful commands\n;current (location) - Current weather information for that location', inline=False)

  await ctx.send(embed=embed)

def get_baseinfo(location, response):
  json_data = json.loads(response.text)
  json_data_current = json_data["current"]
  data = "**Temperature:** " + str(json_data_current["temp_c"]) + " (*°C*) | " + str(json_data_current["temp_f"]) + " (*°F*)\n**Wind Speed:** " + str(json_data_current["wind_mph"]) + " (*mph*) | " + str(json_data_current["wind_kph"]) + " (*kph*)" + "\n**Wind Direction:** " + str(json_data_current["wind_dir"]) + "\n**Pressure:** " + str(json_data_current["pressure_mb"]) + " (*mb*) | " + str(json_data_current["pressure_in"]) + " (*in*)\n**Precipitation:** " + str(json_data_current["precip_mm"]) + " (*mb*) | " + str(json_data_current["precip_in"]) + " (*in*)\n**Humidity:** " + str(json_data_current["humidity"]) + "\n**Cloud:** " + str(json_data_current["cloud"]) + "\n**UV:** " + str(json_data_current["uv"]) + "\n**Gust:** " + str(json_data_current["gust_mph"]) + " (*mph*) | " + str(json_data_current["gust_kph"]) + " (*kph*)"
  return(data)

def get_icon(response):
  json_data = json.loads(response.text)
  json_data_current = json_data["current"]
  json_data_current_condition = json_data_current["condition"]
  image_url = json_data_current_condition["icon"]
  return(image_url)

def get_location(response):
  json_data = json.loads(response.text)
  json_data_location = json_data["location"]
  if json_data_location["region"] == "":
    data = json_data_location["country"]
  else:
    data = json_data_location["region"] + ", " + json_data_location["country"]
  return data

def get_timedate(response):
  json_data = json.loads(response.text)
  json_data_location = json_data["location"]
  data = json_data_location["localtime"]
  return(data)

@client.command()
async def current(ctx, arg):
  response = requests.get("http://api.weatherapi.com/v1/current.json?key=" + apikey + "&q=" + arg + "&aqi=no")
  image = "https:" + get_icon(response)
  print(image)
  embed = discord.Embed(
    title = get_location(response),  
    color = discord.Color.blue(),
  )
  embed.set_footer(text="localtime: " + get_timedate(response))
  embed.set_author(name='Weather Bot',icon_url='https://cdn.discordapp.com/attachments/909115750218862592/935301531601875014/weather02-512.png')
  embed.add_field(name="Weather Information", value=get_baseinfo(arg, response), inline=False)
  embed.set_thumbnail(url=image)
  
  await ctx.send(embed=embed)