#!/bin/env python3.6
import skinbay
import discord
import base64, asyncio
from datetime import timedelta, datetime
import logging
logging.basicConfig(filename='log.txt', filemode='w')

TOKEN= "YOUR TOKEN HERE"

CHANNEL_ID = CHANNEL ID HERE

# API_KEY= "SKINBAY API KEY HERE""

# my_secret= 'SKINBAY SECRET HERE'

client = discord.Client()

def get_embed(item):
	embed=discord.Embed(title=item.name, url= item.url, color=0x8000ff)
	embed.set_author(name="Skinbay Bot", url="https://www.steadysoles.com/",icon_url="https://pbs.twimg.com/profile_images/1142950465782669313/YvG8n7YA_400x400.png")
	# embed.set_thumbnail(url=item.image)
	embed.add_field(name="Price:", value="${}".format(item.price))
	embed.add_field(name="Discount:", value="{}%".format(item.reduction), inline=True)
	if item.available:
		tmp= "Instantly Withdrawable"
	else:
		# tmp= str(timedelta(seconds= item.available_in))
		tmp = "Not available"
	embed.add_field(name="Availability:", value=tmp, inline=True)
	embed.add_field(name="Suggested Price:", value="${}".format(item.suggested_price), inline=True)
	embed.add_field(name="Profit:", value="${}".format(item.margin), inline=True)
	embed.set_footer(text="Made by Aqyl#0001 | {}".format(datetime.now()), icon_url="https://cdn.discordapp.com/avatars/209007491713990656/53c679c5a86fa33c3bb9631626e80589.png?size=512")
	return embed

async def status_task(channel, wait_time= 60* 5):
	while True:
		print("Updated on: {}".format(datetime.now()))
		# code= pyotp.TOTP(my_secret)
		try:
			items= skinbay.get_items()
			for item in items:
				await channel.send(embed=get_embed(item))
		except Exception as e:
			print(e)
			logging.exception(e)
		await asyncio.sleep(wait_time)

@client.event
async def on_ready():

	wait_time= 60 * 10 # 10 mins in this case

	print('CSGO Skinbay Bot')
	print('Made by Aqyl#0001')
	print('Version 1.0.0')
	print('')
	print('Logged in as:')
	print(client.user.name)
	print('------------------------------------------')
	channel = client.get_channel(CHANNEL_ID)
	print(type(channel))
	client.loop.create_task(status_task(channel, wait_time))
	

try:
	client.run(TOKEN)
except:
	print("Couldn't connect to the Discord Server.")
