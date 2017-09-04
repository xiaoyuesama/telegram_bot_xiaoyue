#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

import telebot
from telebot import types

# 全局参数
API_TOKEN = "Token"
admin_id = int(Your_id)
bot = telebot.TeleBot(API_TOKEN)
# 用来存储群组信息
group_infors = []


# 处理 start 请求 并提供说明
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '欢迎使用入群申请机器人。')  # send the generated help page
    unique_code = message.text.lstrip('/start ')
    join_group(message)


@bot.message_handler(commands=['join'])
def send_welcome(message):
    unique_code = message.text.lstrip('/join ')
    join_group(message)


def join_group(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        unique_code = message.text.lstrip('/start ')
        if unique_code in (-1001119951412,):
            bot.send_message(message.chat.id, '您要申请加入的群是： ' + group_name + ' 以下是入群的验证条件请仔细阅读：' + group_rule)
        else:
            bot.send_message(message.chat.id, "您要申请的群是？ 请通过 /join XXXXX 申请加入相应群聊")
    except Exception:
        bot.send_message(message.chat.id, '啊咧，你在干什么？ 如有疑问请联系 @xiaoyue_sama 。')


# 对于命令 /get_admin 获取群管理狗U•ェ•*U 并显示
@bot.message_handler(commands=['get_admin'])
def to_get_chat_administrators(message):
    get_administrator = bot.get_chat_administrators(message.chat.id)
    administrators = []
    for admin in get_administrator:
        administrator = '@' + str(admin.user.username) + ' '
        administrators.append(administrator)
    admin = ",".join(administrators)
    bot.send_message(message.chat.id, '本群的🐶管理是：' + str(admin) + '。')


# inlinemarkup 相关设置 有生成邀请链接 提供inline button 功能
@bot.message_handler(commands=['inlinemarkup'])
def test_send_message_with_inlinemarkup(message):
    bot.send_message(message.chat.id, '正在生成入群链接')
    text = '您好这是您要加入的群的相应信息'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("群规", url="http://www.google.com"))
    markup.add(types.InlineKeyboardButton("入群", url=str(
        bot.export_chat_invite_link('-1001119951412'))))  # -1001119951412 为频道唯一ID 如果要使用'@channelusername'的话无比带上'@'
    markup.add(types.InlineKeyboardButton("Yahoo0",
                                          callback_data='yes|' + str(message.chat.id) + str(message.text).lstrip(
                                              '/inlinemarkup')))
    ret_msg = bot.send_message(message.chat.id, text, disable_notification=True, reply_markup=markup)
    assert ret_msg.message_id


@bot.message_handler(commands=['add_new_group_infor'])
def add_new_group_infor(message):
    """完成添加一个新的群组信息"""

    bot.send_message(message.chat.id,
                     "请输入群组的唯一ID或公开群名（群名带@ 例如/add_new_group_infor @Coser_Album）PS：务必是超级群并且本bot成为管理员否则不能生成邀请链接")
    try:
        unique_code = message.text.lstrip('/add_new_group_infor ')
        test = bot.export_chat_invite_link(str(unique_code))
        if test == True:
            Chat_infor = bot.get_chat(unique_code)
            # 定义一个新的字典,用来存储一个新的群组信息
            new_infor = {}
            new_infor['name'] = Chat_infor.username
            new_infor['type'] = Chat_infor.type
            new_infor['description'] = Chat_infor.description
            new_infor['invite_link'] = Chat_infor.invite_link

            # 将一个字典,添加到列表中
            global group_infors
            group_infors.append(new_infor)
        else:
            bot.send_message(message.chat.id, '啊咧，你在干什么？ 请确认您输入了正确的信息 如有疑问请联系 @xiaoyue_sama 。')
    except Exception:
        bot.send_message(message.chat.id, '啊咧，你在干什么？ 请确认您输入了正确的信息 如有疑问请联系 @xiaoyue_sama 。')


@bot.message_handler(commands=['list'])
def list_group_infor(message):
    global group_infors
    group_text = "HI, " + str(message.chat.username) + " 我目前拥有的群组消息: \n"
    for temp in group_infors:  # generate help text out of the group_infors dictionary defined at the top
        group_text += "群组：" + temp['name'] + "描述 " + temp['description'] + "\n"
    bot.send_message(message.chat.id, group_text)  # send the generated group info page


'''
#群组查找
@bot.message_handler(commands=['find'])
def find_group_infor(message):
    """用来查询一个群组"""

    global group_infors

    find_name = input("请输入要查找的群名:")
    find_flag = 0  # 默认表示没有找到
    for temp in group_infors:
        if find_name == temp["name"]:
            print("%s\t%s\t%s\t%s" % (temp['name'], temp['type'], temp['description']))
            find_flag = 1  # 表示找到了
            break

    # 判断是否找到了
    if find_flag == 0:
        print("查无此群组....")
'''


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
