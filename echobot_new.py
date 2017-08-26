#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep

import telegram
from telegram.error import NetworkError, Unauthorized

#设定全局的变量
update_id = None
TOKEN = "420662445:AAGYiyWTqG1Y_KmfFcFHJgUjZZIZqE0KTO0"

def main():
    global update_id
    # 得到telegram bot 的Token 的赋值
    bot = telegram.Bot(TOKEN)

    #获取第一个待处理的 update_id ，以防万一做一个异常处理
    #我们设定一个“未经授权”的异常。
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            #用户已经删除或已拉黑bot.
            update_id += 1


def echo(bot):
    global update_id
    # 在最新一个update_id后请求更新
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # 你的机器人可能收到没有消息的更新
            # 回复消息
            update.message.reply_text(update.message.text)


if __name__ == '__main__': #防止其他程序调用时出现问题
    try:
        main()
    except KeyboardInterrupt: #定义了 Ctrl + C 结束程序的时候出现异常的返回
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)