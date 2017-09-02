#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
import time

import requests
import telebot
from telebot import types

# ========================#
# 以下全局参数设定

API_TOKEN = "TOKEN"
admin_id = int(Your_ID)
hitokoto_api = 'http://api.hitokoto.cn/?encode=text'
hideBoard = types.ReplyKeyboardRemove()  # 隐藏键盘
commands = {  # command description used in the "help" command
    'prpr': 'prpr me',
    'get_chat_id': '得到您的会话ID',
    'hitokoto': '得到一条很有道理但是没啥用的梦呓',
    'help': '获得帮助'
}
# ========================#
'''
老代码用与查看使用者发送给bot的消息
# 转发使用者发给与bot的对话
def ret_msg_to_admin(message):
    # todo 顺带将bot的发送也转发给作者
    bot.forward_message(admin_id, message.chat.id, message.message_id, disable_notification=True)
    # bot.forward_message(admin_id, message.chat.id, msg.message_id, disable_notification=True)
'''


# 显示在控制台
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            bot.send_message(admin_id, str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


# 注册对象
bot = telebot.TeleBot(API_TOKEN)
bot.set_update_listener(listener)  # 注册listener


# 开启DEBUG并输出到控制台
# telebot.logger.setLevel(logging.DEBUG)


# 设定全局函数 send_command_message 减少在群组内打扰人的情况(回复一个消息
def send_command_message(message, text):
    if "group" in message.chat.type:
        if "@xiaoyuesama_bot" in message.text:
            bot.reply_to(message, text)
    else:
        bot.reply_to(message, text)


# 设定全局函数 send_message 减少在群组内打扰人的情况（发送一个单独的消息
def send_message_one(message, text):
    if "group" in message.chat.type:
        if "@xiaoyuesama_bot" in message.text:
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, text)


# 菜单函数在用户使用 /help 的时候显示相应的功能按钮
def muen(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    itembtn_get_chat_id = types.KeyboardButton('/get_chat_id')
    itembtn_prpr = types.KeyboardButton('/prpr')
    itembtn_help = types.KeyboardButton('/help')
    itembtn_hitokoto = types.KeyboardButton('/hitokoto')
    itembtn_lgy = types.KeyboardButton('/lgy')
    itembtn_makedown = types.KeyboardButton('/makedown')
    markup.row(itembtn_hitokoto, itembtn_help, itembtn_makedown)
    markup.row(itembtn_get_chat_id, itembtn_prpr, itembtn_lgy)

    bot.send_message(message.chat.id, "我有以下功能:", reply_markup=markup)


# 处理 start 请求 并提供说明
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    help_text = "HI, " + str(message.chat.username) + " The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(message.chat.id, help_text)  # send the generated help page


# 处理 help 请求
@bot.message_handler(commands=['help'])
def send_Help_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    muen(message)


# 获取会话id get_chat_id
@bot.message_handler(commands=['get_chat_id'])
def send_Get_chat_id(message):
    send_command_message(message, '您的chat_id为：' + str(message.chat.id) + '''
你的User Name为：''' + str(message.chat.username) + '''
你的来源国家可能为：''' + str(message.from_user.language_code))


# 处理 prpr 请求 70%的概率出现 “才不让呢（哼唧”
@bot.message_handler(commands=['prpr'])
def send_prpr(message):
    if random.random() > 0.7:
        bot.send_chat_action(message.chat.id, 'typing')
        send_command_message(message, '才不让呢（哼唧')
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        prpr = open('./imge/prpr.webp', 'rb')
        bot.send_sticker(message.chat.id, prpr, disable_notification=True)
        send_message_one(message, '我也喜欢你呢')


# todo 增加markdown操作
'''
#makedown
@bot.message_handler(commands=['makedown'])
def send_let_me_google_for_you(message):
   pure_message = message.text.lstrip('/makedown ')
   send_command_message(message, pure_message ,parse_mode='Markdown')
'''


# google 内容直接调用，即让我教你google
@bot.message_handler(commands=['lgy'])
def send_let_me_google_for_you(message):
    long_url = 'https://lmgtfy.com/?q=' + message.text.lstrip('/lgy ')
    send_command_message(message, long_url)


# 使用hitokoto的接口返回一句话的梦呓
@bot.message_handler(commands=['hitokoto'])
def send_hitokoto(message):
    try:
        R = requests.get(hitokoto_api)
        send_message_one(message, R)
    except Exception:
        send_message_one(message, '啊咧，接口好像崩坏了。请再次发送 /hitokoto 或稍后尝试。')


# 处理所有文件的音频文件
# noinspection PyUnusedLocal
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


# todo 入群进行提醒


# todo 设定关键词 自动回复 一天提醒一次


# echo_message_info 返回消息信息 顺带获取内容
@bot.message_handler(func=lambda message: True)
def echo_message_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:

        send_command_message(message, '您的chat_id为：' + str(message.chat.id) + '''
你的User Name为：''' + str(message.chat.username) + '''
消息来源者为：''' + str(message.forward_from.username) + '''
消息来源者id为：''' + str(message.forward_from.id))
    except Exception:
        send_command_message(message, '您的chat_id为：' + str(message.chat.id) + '''
你的User Name为：''' + str(message.chat.username))
        pass


def main_loop():  # 主程序函数
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':  # 防止其他程序调用时出现问题
    try:
        main_loop()
    except KeyboardInterrupt:  # 定义了 Ctrl + C 结束程序的时候出现异常的返回
        print('\nExiting by user request.\n')
        sys.exit(0)
