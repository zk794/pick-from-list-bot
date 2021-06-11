# used https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
import discord
import os
from random import randrange
from keep_alive import keep_alive
from replit import db
# db.keys has the names of any lists the bot has, its object is an array of the list's elements. items numbered 1 to len(list)
# possible additions: get random item and delete it, move random item to a different list, move specific item to a different list, for youtube url display name of video in addition to url

helpmessage = 'Hello! I store lists that you give me and let you randomly select items from the lists.\n\nCommands:\n**!listbot add [phrase] to [list]** -- adds the phrase as an item in the list. If the list does not exist, it will be created.\n**!listbot listall** -- lists names of all lists in my system.\n**!listbot list [listname]** -- lists all items in the given list.\n**!listbot numitems [list]** -- tells you how many items are in the given list.\n**!listbot delete [item number] from [list]** -- deletes the item with that number from the given list. You can find out the number of an item by listing all of them. It will also be shown next to an item selected with the random command.\n**!listbot deletelist [listname]** -- deletes the entire list, as if it never existed.\n**!listbot random [listname]** -- picks a random item from the list for you.\n**!listbot random [listname] and [listname]...** -- picks a random item from multiple lists combined. Use as many ands as you wish.\n**!listbot** -- summon this help message!\n'

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # send message containing random item in list(s)
  if msg.startswith('!listbot random '):
    n = msg[len('!listbot random '):]
    lists = n.split(' and ')
    masterlist = []
    listlens = []
    doThing = True
    for listname in lists:
      if (listExists(listname)):
        for item in db[listname]:
          masterlist.append(item)
        listlens.append(len(db[listname]))
      else:
        print('error in random command')
        await message.channel.send(f'Error: the list {listname} doesn\'t exist. Use the add command to create a new list. Send \"!listbot\" for help.')
        doThing = False
    if doThing:
      x = randrange(len(masterlist))
      listind = 0
      totlen = listlens[0]
      print(x, listind, totlen)
      while x >= totlen:
        listind = listind + 1
        totlen = totlen + listlens[listind]
        print(listind, totlen)
      totlen = totlen - listlens[listind]
      print(listind, totlen)
      print(f'Random item is from {lists[listind]}:\n{x-totlen+1}: {masterlist[x]}')
      await message.channel.send(f'Random item is from {lists[listind]}:\n{x-totlen+1}: {masterlist[x]}')

  # add item to a list
  elif msg.startswith('!listbot add '):
    command = msg[len('!listbot add '):]
    if (command.find(' to ') > -1):
      item = command.partition(' to ')[0]
      listname = command.partition(' to ')[2]
    else:
      await message.channel.send('Error: bad formatting for add command. Format is \"!listbot add [string] to [name of a list]\"')
      return
    x = addToList(item, listname)
    print(x)
    await message.channel.send(x)

  # list all items in list
  elif msg.startswith('!listbot list '):
    listname = msg[len('!listbot list '):]
    if listExists(listname):
      st = f'{listname} contains {len(db[listname])} items:\n'
      num = 1
      for item in db[listname]:
        st = st + str(num) + ': ' + item + '\n'
        num = num + 1
      await message.channel.send(st)
      print(f'listed items in {listname}')
    else:
      await message.channel.send(f'Error: the list {listname} doesn\'t exist. Use the add command to create a new list. Send \"!listbot\" for help.')
      print(f'error when listing {listname}')

  # list lists
  elif msg.startswith('!listbot listall'):
    st = 'Here are your lists:\n'
    for item in db.keys():
      st = st + '\n' + item
    await message.channel.send(st)
    print(st)

  # find number of items in list
  elif msg.startswith('!listbot numitems '):
    listname = msg[len('!listbot numitems '):]
    if listExists(listname):
      await message.channel.send(f'{listname} contains {len(db[listname])} items:\n')
      print(f'{listname} contains {len(db[listname])} items:\n')
    else:
      await message.channel.send(f'Error: the list {listname} doesn\'t exist. Use the add command to create a new list. Send \"!listbot\" for help.')
      print(f'error printing numitems in {listname}')

  # delete item from a list
  elif msg.startswith('!listbot delete '):
    command = msg[len('!listbot delete '):]
    if (command.find(' from ') > -1):
      try:
        index = int(command.partition(' from ')[0])
      except:
        await message.channel.send('Error: bad formatting for delete command. Send \"!listbot\" for help.')
        print('bad index for delete')
      listname = command.partition(' from ')[2]
    else:
      await message.channel.send('Error: bad formatting for delete command. Send \"!listbot\" for help.')
      print('delete command error 1')
      return
    if (index-1) > len(db[listname]):
      await message.channel.send(f'There is no item {index}.')
      return
    try:
      deleteFromList(index-1, listname)
      await message.channel.send(f'Deleted item number {index} from {listname}.')
      print(f'deleted item from {listname}')
    except:
      await message.channel.send('Error: bad formatting for delete command. Send \"!listbot\" for help.')
      print('delete command error 2')

  # delete a list
  elif msg.startswith('!listbot deletelist '):
    listname = msg[len('!listbot deletelist '):]
    try:
      deleteList(listname)
      await message.channel.send(f'Deleted {listname}.')
      print(f'deleted {listname}')
    except:
      await message.channel.send(f'Error: could not delete {listname}.')
      print(f'could not delete {listname}')

  elif msg.startswith('!listbot'):
    # add help message
    # list names must contain no whitespace
    await message.channel.send(helpmessage)
    print('Hello!')

def listExists(listname):
  if listname in db.keys():
    return True
  else:
    return False

def addToList(item, listname):
  if listname in db.keys():
    list = db[listname]
    list.append(item)
    db[listname] = list
    return f'Done! \"{listname}\" now contains \"{item}\".'
  else:
    db[listname] = [item]
    return f'Created new list called {listname} containing \"{item}\"'

def deleteFromList(index, listname):
  list = db[listname]
  if len(list) > index:
    del list[index]
  db[listname] = list
  return f'Item number {index} has been deleted from {listname}. {listname} now contains {len(db[listname])} items.'

def deleteList(listname):
  del db[listname]

keep_alive()
client.run(os.environ['TOKEN'])
