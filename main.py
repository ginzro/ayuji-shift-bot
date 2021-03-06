import discord
import os
import boto3
import datetime
from aiohttp import TCPConnector

import logging
logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

logging.basicConfig()
logging.getLogger('bot').setLevel(level=logging.INFO)


MSG = None
HELP_MESSAGE = """[コマンドリスト]
$help                      :このメッセージを表示
$shift                     :シフト表示
@ayuji-shift-bot ${予定}   :${予定}部分を登録します
"""


def setup_client():
    return discord.Client()


def setup_event(client, bucket):
    @client.event
    async def on_ready():
        logger.info('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        global MSG
        if message.author == client.user:
            return

        if message.content.startswith('$shift'):
            if MSG is None:
                MSG = get_s3(bucket, 'shift.txt')

            logger.info(str('send shift message: ' + MSG))
            await message.channel.send(MSG)

        if message.content.startswith('$help'):
            logger.info(str('send help message'))
            await message.channel.send(HELP_MESSAGE)

        if client.user in message.mentions:
            MSG = build_msg(message.content)
            put_s3(bucket, 'shift.txt', MSG)
            logger.info(str('update shift to ' + MSG))
            await message.channel.send('shift updated!')

def build_msg(rep):
    start_pos = rep.index(' ') + 1
    body = rep[start_pos:]
    return str(body + '\n' + get_today_string())

def get_today_string():
    now = datetime.datetime.today()
    return str('updated at ' + now.strftime("%m/%d %H:%M"))

def get_s3(bucket, key):
    obj = bucket.Object(key)
    res = obj.get()
    body = res['Body'].read()
    logger.info('read ' + key + ' from s3')
    return body.decode('utf-8')

def put_s3(bucket, key, body):
    obj = bucket.Object(key)
    obj.put(
        Body=body.encode('utf-8'),
        ContentEncoding='utf-8',
        ContentType='text/plane'
    )
    logger.info('put ' + key + ' to s3')
    return


def setup_s3_bucket():
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name='ap-northeast-1'
                        )

    BUCKET_NAME = os.environ['BUCKET_NAME']
    return s3.Bucket(BUCKET_NAME)


def main():
    bucket = setup_s3_bucket()
    client = setup_client()
    setup_event(client, bucket)

    DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
    client.run(DISCORD_BOT_TOKEN)


main()
