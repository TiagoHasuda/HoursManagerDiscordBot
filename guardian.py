import os
from datetime import datetime, timedelta
from constants import Constants

path = r'/projects/discordBots/hoursManager/archive/'
dateFormat = '%d%m%Y'
timeFormat = '%H:%M:%S'

def renameDir(userTag,userId):
  if os.path.isdir(path + userTag):
    os.rename(path + userTag, path + userId)

def getToday():
  currDate = datetime.today() - timedelta(hours=3, minutes=0)
  return currDate.strftime(dateFormat)

def getTime():
  currDate = datetime.today() - timedelta(hours=3, minutes=0)
  return currDate.strftime(timeFormat)

def getUserPath(name,refDate=''):
  if refDate == '':
    refDate = getToday()
  return path + name + '/' + refDate + '.txt'

def checkUserExists(name):
  return os.path.isdir(path + name)

def checkDateExists(name,date):
  return os.path.isfile(path + name + '/' + date + '.txt')

def checkRunning(name,refDate=''):
  isRunning = False
  userPath = getUserPath(name, refDate)
  if os.path.isfile(userPath):
    userFile = open(userPath, 'r')
    lastLine = userFile.readlines()[-1]
    isRunning = not (lastLine.startswith(Constants.STOP) or lastLine.startswith(Constants.PAUSE))
    userFile.close()
  return isRunning

def write(name,content,refDate=''):
  if refDate == '':
    refDate = getToday()
  if not checkUserExists(name):
    os.mkdir(path + name)
  dateFile = open(path + name + '/' + refDate + '.txt', 'a+')
  dateFile.write(content + '\n')
  dateFile.close()

def startString():
  return Constants.START + Constants.SEPARATOR + getTime()

def stopString(notToday = False):
  if not notToday:
    return Constants.STOP + Constants.SEPARATOR + getTime()
  else:
    return Constants.STOP + Constants.SEPARATOR + '23:59:59'

def pauseString():
  return Constants.PAUSE + Constants.SEPARATOR + getTime()

def messageString(message):
  return Constants.MESSAGE + Constants.SEPARATOR + getTime() + Constants.SEPARATOR + message

def start(name):
  if checkRunning(name):
    return 'Already started'
  write(name, startString())
  return 'Started'

def pause(name):
  if not checkRunning(name):
    return 'You need to run !start first'
  write(name, pauseString())
  return 'Paused'

def stop(name):
  if not checkRunning(name):
    return 'You need to run !start first'
  write(name, stopString())
  return 'Stopped'

def restart(name):
  if not checkRunning(name):
    return 'You need to run !start first'
  write(name, stopString())
  write(name, startString())
  return 'Restarted'

def message(name,message):
  if not checkRunning(name):
    return 'You need to run !start first'
  if not message:
    return 'Message empty, nothing done'
  write(name, messageString(message))
  return 'Message saved'

def summary(name,date):
  userPath = path + name + '/'
  if not date:
    date = getToday()
  userPath += date + '.txt'
  if not os.path.isfile(userPath):
    return 'Data for given date not found'
  returnString = ''
  if checkRunning(name) and date == getToday():
    returnString += 'Still running...report will be incomplete\n'
  elif checkRunning(name,date):
    write(name,stopString(True),date)
  returnString += '```\n'
  dateFile = open(userPath, 'r')
  fullFile = dateFile.readlines()
  command = ''
  messages = []
  paused = False
  start = datetime.today()
  end = datetime.today()
  total = timedelta(hours=0, minutes=0)
  allTotal = timedelta(hours=0, minutes=0)
  for line in fullFile:
    splits = line.split(Constants.SEPARATOR)
    splits[len(splits) - 1] = splits[len(splits) - 1].replace('\n', '')
    command = splits[0]
    match command:
      case Constants.START:
        print('hm' + splits[1] + '//' + timeFormat)
        start = datetime.strptime(splits[1], timeFormat)
        if start.hour == end.hour and start.minute == end.minute:
          start = start + timedelta(hours=0, minutes=1)
      case Constants.PAUSE:
        end = datetime.strptime(splits[1], timeFormat)
        total += end - start
        allTotal += end - start
        paused = True
      case Constants.STOP:
        end = datetime.strptime(splits[1], timeFormat)
        total += end - start
        allTotal += end - start
        if paused:
          start = end - total
        returnString += start.strftime(timeFormat) + '\t' + end.strftime(timeFormat) + '\nTotal: ' + str(total) + '\nMessage: ' + '\n'.join(messages) + '\n' + Constants.LINE_SEPARATOR + '\n'
        messages = []
        paused = False
        total = timedelta(hours=0, minutes=0)
      case Constants.MESSAGE:
        messages.append(splits[2])
  returnString += '\nTotal time: ' + str(allTotal) + '\n'
  returnString += '```\n'
  n = 1994
  result = [returnString[i:i+n] for i in range(0, len(returnString), n)]
  if len(result) == 1:
    return result
  newResult = []
  for res in result:
    if not res.startswith('```'):
      res = '```' + res
    if not res.endswith('```'):
      res += '```'
    newResult.append(res)
  return newResult
