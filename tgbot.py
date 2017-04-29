#coding:utf-8
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import requests, json, logging

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

isInput = False #存储当前bot是否为等待用户输入型号的状态

def start(bot, update):
    keyboard = [[InlineKeyboardButton("LineageOS", callback_data='los'),
                 InlineKeyboardButton("Mokee", callback_data='mokee')],

                [InlineKeyboardButton("AICP", callback_data='aicp')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose your ROM:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    if query.data=='yes' or query.data=='no':
        bot.editMessageText(text="您选择的是: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
        return

    bot.editMessageText(text="您选择的ROM是: %s\n请输入并发送您的设备型号" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    global selecting
    selecting = True

def normal(bot, update):
    if not isInput:
        text = update.message.text
        update.message.reply_text("您输入的型号是: %s" % text)

        keyboard = [[InlineKeyboardButton("是", callback_data='yes'),
                    InlineKeyboardButton("否", callback_data='no')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('是否只要最新版:', reply_markup=reply_markup)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")



dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, normal))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

updater.idle()
