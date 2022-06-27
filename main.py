import discord
import os
from dotenv import load_dotenv
import guardian

load_dotenv()

client = discord.Client()

botTag = '!'

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  userTag = message.author.name + '#' + message.author.discriminator
  if message.content.startswith(botTag + 'start'):
    try:
      res = guardian.start(userTag)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error starting!' + str(e))
  if message.content.startswith(botTag + 'stop'):
    try:
      res = guardian.stop(userTag)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error stopping!' + str(e))
  if message.content.startswith(botTag + 'restart'):
    try:
      res = guardian.restart(userTag)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error restarting!' + str(e))
  if message.content.startswith(botTag + 'message '):
    try:
      userMessage = message.content.lstrip(botTag + 'message ')
      res = guardian.message(userTag, userMessage)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error saving message!' + str(e))
  if message.content.startswith(botTag + 'summary'):
    try:
      refDate = ''
      if message.content.startswith(botTag + 'summary '):
        refDate = message.content.lstrip(botTag + 'summary ')
      res = guardian.summary(userTag, refDate)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.sned('Error getting summary! ' + str(e))

client.run(os.getenv('TOKEN'))
