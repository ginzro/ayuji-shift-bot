import discord
import os

client = discord.Client()
msg = 'hello!'
help_message = """[コマンドリスト]
$help                      :このメッセージを表示
$shift                     :シフト表示
@ayuji-shift-bot ${予定}   :${予定}部分を登録します
"""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global msg
    if message.author == client.user:
        return

    if message.content.startswith('$shift'):
        await message.channel.send(msg)

    if message.content.startswith('$help'):
        await message.channel.send(help_message)


    if client.user in message.mentions:
        rep = message.content
        start_pos = rep.index(' ') + 1
        msg = rep[start_pos:]
        await message.channel.send('Shift updated to ' + msg)


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
