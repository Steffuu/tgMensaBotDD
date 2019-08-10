#!/bin/python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, json
import os
import logging
from datetime import date, timedelta


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Reichenbach is never an option!")


def echoText(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def echoSticker(update, context):
    sticker = update.message.sticker
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)

def mensa(update, context):
    params = context.args
    if len(params) < 1:
        daysToAdd = 0
    else:
        try:
            daysToAdd = int(params[0])
        except ValueError:
            context.bot.send_message(chat_id=update.message.chat_id, text="The first and only parameter has to be an integer value. Aborting.")
            return
    day = date.today() + timedelta(days=daysToAdd)
    url = "https://openmensa.org/api/v2/canteens/79/days/" + day.strftime("%Y-%m-%d") + "/meals"
    resp = requests.get(url)
    if not resp.ok:
        context.bot.send_message(chat_id=update.message.chat_id, text="I failed miserably. Disgrace!")
        return
    jsonData = json.loads(resp.content)
    for elem in jsonData:
        context.bot.send_message(chat_id=update.message.chat_id, text=elem["name"])


def andre(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Höhöhö Reichenbach!")


def dadJoke(update, context):
    headers = {'Accept': 'text/plain '}
    resp = requests.get("https://icanhazdadjoke.com/", headers=headers)
    if not resp.ok:
        context.bot.send_message(chat_id=update.message.chat_id, text="I failed miserably. Disgrace!")
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=resp.text)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    apiToken = os.environ['TELEGRAM_APITOKEN']
    updater = Updater(token=apiToken, use_context=True)

    startHandler = CommandHandler('start', start)
    updater.dispatcher.add_handler(startHandler)

    mensaHandler = CommandHandler('mensa', mensa)
    updater.dispatcher.add_handler(mensaHandler)

    andreHandler = CommandHandler('andre', andre)
    updater.dispatcher.add_handler(andreHandler)

    dadJokeHandler = CommandHandler('leon', dadJoke)
    updater.dispatcher.add_handler(dadJokeHandler)

    echoHandlerText = MessageHandler(Filters.text, echoText)
    updater.dispatcher.add_handler(echoHandlerText)

    echoHandlerSticker = MessageHandler(Filters.sticker, echoSticker)
    updater.dispatcher.add_handler(echoHandlerSticker)

    updater.start_polling()


if __name__ == "__main__":
    main()