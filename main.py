import discord
import os
from aiohttp import TCPConnector

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
MSG = 'hello!'
HELP_MESSAGE = """[コマンドリスト]
$help                      :このメッセージを表示
$shift                     :シフト表示
@ayuji-shift-bot ${予定}   :${予定}部分を登録します
"""

def setup_client():
    # herokuを使用する上でportは自由に設定することができず動的に与えられるPORTを使用する必要があるため
    PORT = os.getenv('PORT', '8080')
    for_heroku = TCPConnector(local_addr=('0.0.0.0', PORT))
  
    return  discord.Client(connector=for_heroku)


def setup_event(client):
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
    
    @client.event
    async def on_message(message):
        global MSG
        if message.author == client.user:
            return
    
        if message.content.startswith('$shift'):
            print(str('send shift message: ' + MSG))
            await message.channel.send(MSG)
    
        if message.content.startswith('$help'):
            print(str('send help message')
            await message.channel.send(HELP_MESSAGE)
    
    
        if client.user in message.mentions:
            rep = message.content
            start_pos = rep.index(' ') + 1
            msg = rep[start_pos:]
            print(str('update shift to ' + msg)
            await message.channel.send('Shift updated to ' + msg)

def main():
    client = setup_client()
    setup_event(client)
    client.run(DISCORD_BOT_TOKEN)


main()
