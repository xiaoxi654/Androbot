from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests, json, logging

updater = Updater(token='Token')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("LineageOS", callback_data='los'),
                 InlineKeyboardButton("Mokee", callback_data='mokee')],
                
                [InlineKeyboardButton("AICP", callback_data='aicp')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose your ROM:', reply_markup=reply_markup)

              
def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected ROM: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")

    

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()

updater.idle()

