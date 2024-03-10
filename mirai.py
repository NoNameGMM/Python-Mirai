# -*- coding: utf-8 -*-
from java.io import File
from java.net import URL, URLClassLoader
from java.util.function import Consumer
import os
import json

current_directory = os.path.dirname(os.path.abspath(__file__))
bot_file = current_directory + "/bot.json"
with open(bot_file) as f:
    data = json.load(f)
bot_id = data["bot"]
login_type = data["login_type"]
password = data["password"]

mirai_core = File(current_directory + "/libs/mirai-core-all-2.16.0-all.jar")
mirai_core_url = URL("file:" + mirai_core.getAbsolutePath())
mirai_loader = URLClassLoader.newInstance([mirai_core_url])

BotFactory = mirai_loader.loadClass("net.mamoe.mirai.BotFactory")
Bot = mirai_loader.loadClass("net.mamoe.mirai.Bot")
BotConfiguration = mirai_loader.loadClass("net.mamoe.mirai.utils.BotConfiguration")
BotAuthorization = mirai_loader.loadClass("net.mamoe.mirai.auth.BotAuthorization")
Contact = mirai_loader.loadClass("net.mamoe.mirai.contact.Contact")
BotOnlineEvent = mirai_loader.loadClass("net.mamoe.mirai.event.events.BotOnlineEvent")
GroupMessageEvent= mirai_loader.loadClass("net.mamoe.mirai.event.events.GroupMessageEvent")
PlainText = mirai_loader.loadClass("net.mamoe.mirai.message.data.PlainText")
BotConfiguration = mirai_loader.loadClass("net.mamoe.mirai.utils.BotConfiguration")
DeviceInfo = mirai_loader.loadClass("net.mamoe.mirai.utils.DeviceInfo")
AbstractBotConfiguration = mirai_loader.loadClass("net.mamoe.mirai.utils.AbstractBotConfiguration")

def login():
    cacheDir = File("cache")
    bot.configuration.fileBasedDeviceInfo(current_directory + "device.json")
    bot.configuration.protocol = BotConfiguration.MiraiProtocol.ANDROID_WATCH
    class BotEventHandler:
    
        @staticmethod
        def send_message_on_login(event):
            if isinstance(event, BotOnlineEvent):
                print(u"登录成功，开始发送消息")
                bot = event.getBot()
                target_group = bot.getGroup(820819698)  # 替换为您要发送消息的群组的群号
                target_group.sendMessage(PlainText(u"你好!我拥有生命了!"))

        @staticmethod
        def reply_to_group_message(event):
            if isinstance(event, GroupMessageEvent):
                message = event.getMessage()
                group = event.getGroup()
                if group.id == 820819698:  # 替换为您要回复消息的群组的群号
                    message_content = PlainText(u"收到您的消息: " + message.contentToString())
                    group.sendMessage(message_content)


    # 创建事件处理类的实例
    event_handler = BotEventHandler()

    class BotOnlineEventConsumer(Consumer):
        def accept(self, event):
            event_handler.send_message_on_login(event)

    class GroupEventConsumer(Consumer):
        def accept(self, event):
            event_handler.reply_to_group_message(event)

    # 创建Consumer实例
    bot_online_consumer = BotOnlineEventConsumer()
    group_message_consumer = GroupEventConsumer()

    # 使用Consumer实例作为事件处理方法
    bot.getEventChannel().subscribeAlways(BotOnlineEvent, bot_online_consumer)
    bot.getEventChannel().subscribeAlways(GroupMessageEvent, group_message_consumer)
    bot.login()

if (login_type == 'QRCode'):
    bot = BotFactory.INSTANCE.newBot(bot_id, BotAuthorization.byQRCode())
    login()
elif (login_type == 'Password'):
    bot = BotFactory.INSTANCE.newBot(bot_id, password)
    login()
else:
    print(u"登陆信息错误,请重试")