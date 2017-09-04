#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import random
import sys
import time

import requests
import telebot
from telebot import types

# ========================#
# 以下全局参数设定

API_TOKEN = "Token"
admin_id = int(yourID)
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
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


# 设定全局函数 send_command_message 减少在群组内打扰人的情况(回复一个消息
def send_command_message(message, text):
    if "group" in message.chat.type:
        if "@xiaoyuesama_bot" in message.text:
            bot.reply_to(message.chat.id, text)
    else:
        bot.reply_to(message.chat.id, text)


# 设定全局函数 send_message 减少在群组内打扰人的情况（发送一个单独的消息
def send_message_one(message, text):
    if "group" in message.chat.type:
        if "@xiaoyuesama_bot" in message.text:
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, text)


# 菜单函数在用户使用 /help 的时候显示相应的功能按钮
def muen(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=0)
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


# 发送chatid 检测频道的唯一id（Unique identifier）
@bot.message_handler(commands=['Chat'])
def send_getChat_id(message):
    try:
        L = message.text.lstrip('/Chat ')
        Chat_L_Id = bot.get_chat(L)
        if Chat_L_Id.type == "supergroup":
            bot.send_message(message.chat.id, '该超级群的唯一id（Unique identifier）为：' + str(Chat_L_Id.id))
        else:
            bot.send_message(message.chat.id, '该频道的唯一id（Unique identifier）为：' + str(Chat_L_Id.id))
    except Exception:
        bot.send_message(message.chat.id, '返回错误消息不正确，可能是因为提供数据不是超级群或频道。')


# inlinemarkup 相关设置 有生成邀请链接 提供inline button 功能
@bot.message_handler(commands=['inlinemarkup'])
def test_send_message_with_inlinemarkup(message):
    try:
        text = '测试信息'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Google", url="http://www.google.com"))
        markup.add(types.InlineKeyboardButton("Yahoo", url="https://t.me/Cosplay_Album"))
        markup.add(types.InlineKeyboardButton("Yaho00o", url=str(
            bot.export_chat_invite_link('-1001119951412'))))  # -1001119951412 为频道唯一ID 如果要使用'@channelusername'的话无比带上'@'
        markup.add(types.InlineKeyboardButton("Yahoo0",
                                              callback_data='yes|' + str(message.chat.id) + str(message.text).lstrip(
                                                  '/inlinemarkup')))
        ret_msg = bot.send_message(message.chat.id, text, disable_notification=True, reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, '啊咧，接口好像没有返回成功。本 bot 似乎没有成为管理员。')

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    logger.info(call)


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


# 发送 makedown 化后的消息
@bot.message_handler(commands=['makedown'])
def send_markdown_for_you(message):
   pure_message = message.text.lstrip('/makedown ')
   bot.send_message(message.chat.id, pure_message, parse_mode="Markdown")


# 发送 HTML 化后的消息
@bot.message_handler(commands=['html'])
def send_html_for_you(message):
    pure_message = message.text.lstrip('/html ')
    bot.send_message(message.chat.id, pure_message, parse_mode="HTML")



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


# 对于命令 /get_admin 获取群管理狗U•ェ•*U 并显示
@bot.message_handler(commands=['get_admin'])
def to_get_chat_administrators(message):
    get_administrator = bot.get_chat_administrators(message.chat.id)
    administrators = []
    for admin in get_administrator:
        administrator = '@' + str(admin.user.username) + ' '
        administrators.append(administrator)
    admin = ",".join(administrators)
    send_message_one(message, '本群的🐶管理是：' + str(admin) + '。')


# 入群进行提醒
@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def handle_new_chat_member(message):
    bot.send_message(message.chat.id, '亲爱的 ' + message.new_chat_member.username + ' 你吼呀，欢迎加入本群。')


# todo 设定关键词 对于特定的人 自动回复 一天提醒一次
'''
设定相应的加群指令 md5（群名）
1.自动获取相应群 群内管理员及其创造者，并记录

2.当获取到加群申请时 对相应的群的申请信息发送至相应的管理者

3.当管理员同意的时候（只需管理员点击一个按钮即可(Inline keyboards and on-the-fly updating)
最好所有管理员接触到的按钮同步）

    两种方案
    1.bot与管理员私聊
    2.创建一个频道
4.管理员同意后拉人进群
'''
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
