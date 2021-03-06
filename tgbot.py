# -*- coding:utf-8 -*-  

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

import requests, json, logging

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    # 添加消息处理 handler -> selectRom
    dispatcher.add_handler(MessageHandler(Filters.text, selectRom))
    
    # 构建键盘按钮
    keyboard = [[KeyboardButton("LOS")],
                [KeyboardButton("Mokee")],
                [KeyboardButton("AICP")]]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard='true')
    
    update.message.reply_text('Please choose your ROM from below:\nAICP\nLineage OS\nMoKee', reply_markup=reply_markup)

def selectRom(bot, update):
    dispatcher.remove_handler(dispatcher.handlers[0][2])
    # 添加消息处理 -> checkDevice
    dispatcher.add_handler(MessageHandler(Filters.text, checkDevice))
    
    # 删除键盘
    reply_markup = ReplyKeyboardRemove()
    
    # 检查ROM类型
    if update.message.text.lower() in ['aicp', 'los', 'mokee']:
        global romType
        romType = update.message.text.lower()
        update.message.reply_text("Great, %s selected.\nAnd please tell me your device name" % romType.upper(), reply_markup=reply_markup)
        

def checkDevice(bot, update):
    global deviceName
    deviceName = update.message.text.lower()
    # 确认设备是否存在
    check = requests.get('http://api.termux-cn.tk/%s/%s/check' % (deviceName, romType))
    if check.json()['code'] == 200 :
        getAPI(bot, update)
    else :
        update.message.reply_text(check.json()['msg'])
    
    # 取消消息处理
    dispatcher.remove_handler(dispatcher.handlers[0][2])

def getAPI(bot, update):
    # 构建WEB请求调用API
    result = requests.get('http://api.termux-cn.tk/%s/%s/lastest' % (deviceName, romType))
    result = result.json()
    
    # 回复用户
    update.message.reply_text("Filename: %s\nSize: %s\nURL: %s\nMD5：%s\nChangelog: %s" % (result['name'], result['size'], result['url'], result['md5'], result['log']))

def help(bot, update):
    update.message.reply_text("Use /getrom to test this bot.")



dispatcher.add_handler(CommandHandler('getrom', start))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()

updater.idle()
