# -*- coding: utf-8 -*-
import asyncio

import blivedm
import blivedm.models.open_live as open_models
import blivedm.models.web as web_models
from Windows import MainWindowUI
from GPT import Chat
from Utils import Config, Common
import os
import sys
import threading
import gc
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import requests


MAIN_WINDOW = MainWindowUI()
LIVE_MSG_CONTENT = ""
PENDING_LIST = []


async def main():
    await run_bilibili_client()


async def run_bilibili_client():
    """
    演示监听一个直播间
    """
    client = blivedm.OpenLiveClient(
        access_key_id=Config().get_access_key_id(),
        access_key_secret=Config().get_access_key_secret(),
        app_id=Config().get_app_id(),
        room_owner_auth_code=Config().get_room_owner_auth_code(),
    )
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        await client.join()
    finally:
        await client.stop_and_close()


class MyHandler(blivedm.BaseHandler):
    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        # print(f'[{client.room_id}] 心跳')
        pass

    def _on_open_live_danmaku(self, client: blivedm.OpenLiveClient, message: open_models.DanmakuMessage):
        print(f'[{message.room_id}] {message.uname}：{message.msg}')
        global PENDING_LIST
        PENDING_LIST.append(message)
        MAIN_WINDOW.update_wait_list_signal.emit(PENDING_LIST)

    def _on_open_live_gift(self, client: blivedm.OpenLiveClient, message: open_models.GiftMessage):
        coin_type = '金瓜子' if message.paid else '银瓜子'
        total_coin = message.price * message.gift_num
        print(f'[{message.room_id}] {message.uname} 赠送{message.gift_name}x{message.gift_num}'
              f' （{coin_type}x{total_coin}）')

    def _on_open_live_buy_guard(self, client: blivedm.OpenLiveClient, message: open_models.GuardBuyMessage):
        print(f'[{message.room_id}] {message.user_info.uname} 购买 大航海等级={message.guard_level}')

    def _on_open_live_super_chat(
        self, client: blivedm.OpenLiveClient, message: open_models.SuperChatMessage
    ):
        print(f'[{message.room_id}] 醒目留言 ¥{message.rmb} {message.uname}：{message.message}')

    def _on_open_live_super_chat_delete(
        self, client: blivedm.OpenLiveClient, message: open_models.SuperChatDeleteMessage
    ):
        print(f'[{message.room_id}] 删除醒目留言 message_ids={message.message_ids}')

    def _on_open_live_like(self, client: blivedm.OpenLiveClient, message: open_models.LikeMessage):
        print(f'[{message.room_id}] {message.uname} 点赞')


def process_pending_list():
    global PENDING_LIST
    while True:
        if len(PENDING_LIST) > 0:
            message = PENDING_LIST.pop(0)
            MAIN_WINDOW.update_ask_bilibili_signal.emit(message)
            chat = Chat(Config().get_api_key())
            answer = chat.chat(message.msg, stream=True)
            answer_content = ''
            for char in answer:
                answer_content += char
                MAIN_WINDOW.update_answer_signal.emit(answer_content)
            MAIN_WINDOW.update_wait_list_signal.emit(PENDING_LIST)
            gc.collect()


def process_wait_list(wait_list: list):
    # convert list to string and update
    wait_list_str = ''
    for i in wait_list:
        wait_list_str += f"{i.uname}: {i.msg}\n\n"
    MAIN_WINDOW.labelWaitList.setText(wait_list_str)


def update_ask_msg(msg: blivedm.models.open_live.DanmakuMessage):
    MAIN_WINDOW.textEdit_2.setText(msg.msg)
    MAIN_WINDOW.labelUsername.setText(f"@{msg.uname}")
    # rep = requests.get(get_user_avatar(msg.uid))
    rep = requests.get(msg.uface)
    try:
        if rep.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(rep.content)

            # round avatar
            MAIN_WINDOW.labelUserLogo.setPixmap(Common.round_avatar(pixmap))
    except:
        # load default avatar
        MAIN_WINDOW.labelUserLogo.setPixmap(Common.round_avatar(QPixmap("Resources/bilibili_default_avatar.jpg")))
    MAIN_WINDOW.labelUserLogo.setScaledContents(True)

def update_answer_msg(msg: str):
    MAIN_WINDOW.textEdit.setMarkdown(msg)
    # scroll to bottom
    MAIN_WINDOW.textEdit.moveCursor(MAIN_WINDOW.textEdit.textCursor().End)

def run_main_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MAIN_WINDOW.setupUi(MainWindow)
    MAIN_WINDOW.update_ask_bilibili_signal.connect(update_ask_msg)
    MAIN_WINDOW.update_answer_signal.connect(update_answer_msg)
    MAIN_WINDOW.update_wait_list_signal.connect(process_wait_list)
    MainWindow.setWindowTitle("Bilibili Chatbot")
    MainWindow.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    
    if Config().is_proxy_on():
    # set proxy for openai API
        os.environ["HTTP_PROXY"] = Config().get_proxy_url
        os.environ["HTTPS_PROXY"] = Config().get_proxy_url
        
    # thread run main window
    thread_main_window = threading.Thread(target=run_main_window)
    thread_main_window.start()

    # thread process pending list
    thread_process_pending_list = threading.Thread(target=process_pending_list)
    thread_process_pending_list.start()
    asyncio.run(main())
