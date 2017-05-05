# -*- coding:utf-8 -*-  

from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import requests, json, logging

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
                    
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="欢迎来到这里，如果想要获取最新的rom，请输入/help以获取帮助")
    
def getrom(bot, update, args):
    if len(args) == 2:
        checkDevice(bot, update, args)
    else :
        update.message.reply_text("参数有误")
    
def checkDevice(bot, update, args):
    check = requests.get('http://api.termux-cn.tk/%s/%s/check' % (args[1], args[0])).json()
    if check['msg'].lower() == 'success' :
        getAPI(bot, update, args)
    else :
        update.message.reply_text('参数有误!错误原因：\n' + check['msg'])
        
def getAPI(bot, update, args):
    result = requests.get('http://api.termux-cn.tk/%s/%s/lastest' % (args[1], args[0]))
    result = result.json()
    update.message.reply_text("Filename: %s\nSize: %s\nURL: %s\nMD5：%s\nChangelog: %s" % (result['name'], result['size'], result['url'], result['md5'], result['log']))

    
def help(bot, update):
    update.message.reply_text("此机器人的使用方式为/getrom 第三方系统名称 机型代号\n目前支持的第三方系统有AICP(aicp) LineageOS(los) Mokee(mokee)\n机型代号请自行查找")
    
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('getrom', getrom, pass_args=True))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()

updater.idle()
