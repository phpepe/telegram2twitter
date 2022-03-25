#!/usr/bin/env python
import os
from pprint import pprint

from dotenv import dotenv_values
import schedule
import logging

from telethon.tl.types import MessageMediaWebPage, MessageMediaPhoto

from lib import text
from lib.twitter import post_thread
from telethon.sync import TelegramClient

logging.basicConfig(filename='logs/app.log', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

config = dotenv_values()

chat = config.get("tg_chat")
api_id = config.get("tg_api_id")
api_hash = config.get("tg_api_hash")
client = TelegramClient('session_id', api_id, api_hash)
DOWNLOADS_FOLDER = 'storage/downloads'
MESSAGES_TO_PROCESS = 1


def get_last_id():
    """
    Reads the last processed tg message id
    :return:
    """
    with open("LAST_ID.txt", 'r') as file:
        content = file.read()
        if content:
            return int(content)


def process(msg):
    """
    Process telegram message
    :param msg:
    :return:
    """
    logging.info("=======  PROCESSING MESSAGE  id:{id} | date:{date} ======".format(id=msg.id, date=msg.date))
    logging.info("%%%%%%% raw msg:", msg.text)
    img_filename = None
    if isinstance(msg.media, MessageMediaPhoto):
        img_filename = client.download_media(msg, DOWNLOADS_FOLDER)
        logging.info("Has Media: " + img_filename)

    lines = text.split(msg.text, 280, '')
    post_thread(lines, img_filename)
    if img_filename:
        os.remove(img_filename)
    logging.info("%%%%%% split" + str(lines))


def job_telegram():
    """
    Telegram Job (other Jobs in the future?)
    :return:
    """
    with client:
        last_msg = None
        # 10 is the limit on how many messages to fetch. Remove or change for more.
        # client.get_messages(chat)
        # date_time_str = "2021-04-20 16:22:32+00:00"
        # date_from = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
        # for msg in client.iter_messages(chat, 10, offset_date=date_from):
        offset_id = get_last_id()
        for msg in client.iter_messages(chat, MESSAGES_TO_PROCESS, offset_id=offset_id, reverse=True):
            print(msg)

            if msg.media is None or isinstance(msg.media, MessageMediaWebPage) or isinstance(msg.media,
                                                                                             MessageMediaPhoto):
                # Todo if is messageMediaWebpage is link to a tweet, lets re-tweet itØ
                process(msg)
            else:
                logging.info("skipping " + str(msg.id))

            last_msg = msg
            # # save last id
            if last_msg is not None:
                text_file = open("LAST_ID.txt", "w")
            text_file.write(str(last_msg.id))
            text_file.close()


# @ Todo wrap this with scheduler - for now just call this command via cronjob externally
#job_telegram()
