import discord
import os

client = discord.Client()
shifts = [''] * 7
day_of_weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
jap_day_of_weeks = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
help_message = """シフトを表示時する時は$shiftで表示します
シフトを登録するときは${曜日} ${スケジュール}で登録してください
e.x. $mon 15:00 ~ 20:00
曜日リスト ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']"""

def to_shift_string(shifts):
    results = ''
    idx = 0
    for shift in shifts:
        jap = jap_day_of_weeks[idx]
        results += jap + ':' + shift
        results += '\n'
        idx += 1
    return results

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send(help_message)

    if message.content.startswith('$shift'):
        await message.channel.send(to_shift_string(shifts))

    idx = 0
    for day_of_week in day_of_weeks:
        last_schedule = shifts[idx]
        if message.content.startswith('$' + day_of_week[:2]):
            space_idx = message.content.index(' ')
            shifts[idx] = message.content[space_idx:]
            msg = day_of_week + ' schedule updated to ' + shifts[idx] + ' from ' + last_schedule
            await message.channel.send(msg)
        idx += 1


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
