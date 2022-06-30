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
  userId = message.author.id
  guardian.renameDir(userTag, userId)
  if message.content.startswith(botTag + 'start'):
    try:
      res = guardian.start(userId)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error starting!' + str(e))
  if message.content.startswith(botTag + 'stop'):
    try:
      res = guardian.stop(userId)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error stopping!' + str(e))
  if message.content.startswith(botTag + 'restart'):
    try:
      res = guardian.restart(userId)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error restarting!' + str(e))
  if message.content.startswith(botTag + 'message '):
    try:
      userMessage = message.content.lstrip(botTag + 'message ')
      res = guardian.message(userId, userMessage)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error saving message!' + str(e))
  if message.content.startswith(botTag + 'summary'):
    try:
      refDate = ''
      if message.content.startswith(botTag + 'summary '):
        refDate = message.content.lstrip(botTag + 'summary ')
      res = guardian.summary(userId, refDate)
      await message.channel.send(res)
    except Exception as e:
      await message.channel.send('Error getting summary! ' + str(e))
  if message.content.startswith(botTag + 'help'):
    await message.channel.send('```- !start: start counting hours\n- !stop: stop counting hours\n- !restart: stop and start again\n- !message: save a message\n- !summary: returns a summary from today\n- !summary ddMMyyyy: returns a summary for the given date```')

client.run(os.getenv('TOKEN'))
