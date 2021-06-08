import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!listbot'):
        await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))
TOKEN=[ODUxOTU2MjgxNTk3ODg2NDc0.YL_0Hg.gMTZ5EjwPbb7XvDORWmcvmoonnw]
