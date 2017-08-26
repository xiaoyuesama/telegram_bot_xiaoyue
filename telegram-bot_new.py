#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
该Bot使用Updater类来处理机器人。
首先定义一些处理函数。
之后，这些功能被传递给调度程序并登记在各自的位置。
然后，机器人启动并运行，直到我们在命令行上按Ctrl-C。
用法：基本的Echobot示例，Echo消息。
在命令行上按Ctrl-C或发送信号到进程停止机器人。
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

TOKEN = "420662445:AAGYiyWTqG1Y_KmfFcFHJgUjZZIZqE0KTO0"
# 启用日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# 定义几个命令处理程序。 这些通常需要两个参数bot和update。
# error处理程序也会收到引发的 TelegramError 的对象错误。
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('''
我可以提供以下功能
/prpr	prpr me
/get_chat_id	得到您的会话ID
/hitokoto	得到一条很有道理但是没啥用的梦呓
/help	获得帮助''')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # 创建EventHandler并传递您的机器人的token.
    updater = Updater(TOKEN)

    # 获取调度程序来注册处理程序
    dp = updater.dispatcher

    # 对于不同的命令- 在 Telegram 中的回答
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # 对于非命令 使用 echo 来回复
    dp.add_handler(MessageHandler(Filters.text, echo))

    # 记录所以错误
    dp.add_error_handler(error)

    # 启动bot
    updater.start_polling()

    #运行机器人，直到按Ctrl - C或进程接收到SIGINT，
    #SIGTERM或SIGABRT。 这应该是大部分时间使用的，因为start_polling（）是非阻塞的，并会优雅地停止机器人。
    updater.idle()


if __name__ == '__main__': #防止其他程序调用时出现问题
    try:
        main()
    except KeyboardInterrupt: #定义了 Ctrl + C 结束程序的时候出现异常的返回
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)