#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Author__ = "Sewell"

"""
主程序：获取对话信息、记录日志
"""

import os
import codecs
import time
import shutil
import string
import json
import sql
import kw
import itchat
from random import Random
from itchat.content import *

ROOTPATH = "./"
LOGPATH = "./log/"
FILEPATH = "./dlfile/"

create_time = ""
group_id = ""
group_one_id = ""
chat_text = "NULL"
group_chat_text = "NULL"
file_type = "TEXT"
file_name = "NULL"
file_dst = "NULL"
kw_type = "NULL"
kw_word = "NULL"
boss = ""
gchat_count = 0
gchat_kw_count = 0


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
def one_chat(msg):
    """
    获取私聊所有内容，返回指定内容警告并记录言行

    Args:
        [TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO]
        本文、位置、名片、提示、分享、图片、语音、文本、视频

    Returns:
        自定义回复内容

    Demo:
        apiEg/msg_ochat_*.txt

    Future:
        数据进SQLite、Card匹配
    """
    # print(msg)
    if msg['FromUserName'] == msg['User']['UserName']:
        one_id = msg['User']['NickName']
    else:
        one_id = "本机器人"
    file_name = msg['FileName'] # 附件名字
    file_type = msg['Type'] # 附件类型
    chat_text = msg['Text'] # 对话消息文本
    # 未处理!!!
    if type(chat_text) == type('string'):
        chat_text = chat_text.replace('\r', '\\r').replace('\n', '\\n')
    else:
        chat_text = "CARD"
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))  # 消息创建时间
    if file_name:
        chat_text = "NULL"
        TODAYFOLDERPATH = create_today_folder()
        try:
            msg.download(file_name)
            file_src = os.path.join(ROOTPATH, msg['FileName'])
            file_dst_name = random_str(one_id) + '#' + msg['FileName']
            file_dst = TODAYFOLDERPATH + file_dst_name
            shutil.move(file_src, file_dst)
            res = create_time + " dlfile# " + one_id + " " + file_dst_name
            # res = dict(one_id = one_id, create_time = create_time, chat_text = chat_text, file_type = file_type, file_name = file_name, file_dst = file_dst)
            res = json.dumps(res, ensure_ascii=False)
            write_log_one(res + "\n")
            print(res)
        except Exception as e:
            print(e)
    else:
        chat_text = chat_text.replace('\r', '\\r').replace('\n', '\\n')
        res = create_time + " one_chat# " + one_id + " : " + chat_text
        # res = dict(one_id = one_id, create_time = create_time, chat_text = chat_text, file_type = file_type, file_name = file_name, file_dst = file_dst)
        write_log_one(res + "\n")
        print(res)
    
    # 回复指定消息警告
    default_reply = "Default Reply."
    reply = "请不要尝试挑逗机器人，您的言行将被记录." # 回复内容
    return reply or default_reply



@itchat.msg_register([TEXT, MAP, NOTE, SHARING], isGroupChat = True)
def group_chat(msg):
    """
    获取群组聊天文本内容

    Args:
        [TEXT, MAP, NOTE, SHARING]
        本文、位置、提示、分享

    Demo:
        apiEg/msg_gchat_*.txt
    """
    # print(msg)
    global gchat_count, gchat_kw_count
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))
    try:
        group_id = msg.user['NickName']   # 聊天群组ID
    except KeyError as e:
        group_id = "本机器人的群组"
        print(e)
    gchat_count += 1
    group_one_id = msg['ActualNickName']
    if msg['Type'] == "Map":
        group_chat_text = msg['Content'].split(':',1)[0]
    else:
        group_chat_text = msg['Text'].replace('\r', '\\r').replace('\n', '\\n')
    
    # 关键词匹配
    kw_match = kw.demo(group_chat_text)
    if not kw_match:
        kw_type = "NULL"
        kw_word = "NULL"
    else:
        kw_type = kw_match[2]
        kw_word = group_chat_text[kw_match[0]:kw_match[1]]
        # print(kw_type + ' # ' + kw_word)
        gchat_kw_count += 1
        kw_send(group_chat_text, group_id, group_one_id, boss)
    
    # 记录日志
    if group_one_id:
        # res = create_time + " group_chat# " + group_id + " " + group_one_id + " : " + group_chat_text
        # res = str(gchat_count) + " | " + create_time + " | " + group_id + " | " + group_one_id + " | " + group_chat_text + " | " + file_type + " | " + file_name + " | " + file_dst + " | " + kw_word + " | " + kw_type + " | " + str(gchat_kw_count) + " | "
        res = dict(gchat_count = gchat_count, create_time = create_time, group_id = group_id, group_one_id = group_one_id, group_chat_text = group_chat_text, file_type = file_type, file_name = file_name, file_dst = file_dst, kw_word = kw_word, kw_type = kw_type, gchat_kw_count = gchat_kw_count)
    else:
        # res = create_time + " group_chat# " + group_id + " " + "本机器人" + " : " + group_chat_text
        # res = str(gchat_count) + " | " + create_time + " | " + group_id + " | " + "本机器人" + " | " + group_chat_text + " | " + file_type + " | " + file_name + " | " + file_dst + " | " + kw_word + " | " + kw_type + " | " + str(gchat_kw_count) + " | "
        res = dict(gchat_count = gchat_count, create_time = create_time, group_id = "本机器人", group_one_id = group_one_id, group_chat_text = group_chat_text, file_type = file_type, file_name = file_name, file_dst = file_dst, kw_word = kw_word, kw_type = kw_type, gchat_kw_count = gchat_kw_count)
    res = json.dumps(res, ensure_ascii=False)
    write_log_group(res + "\n")
    print(res)
    
    # 插入数据，并更新参数值
    try:
        conn = sql.init()
        sql.insert_gchat(conn, create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type)
        sql.update_var(conn, gchat_count, gchat_kw_count)
        sql.finish(conn)
    except Exception as e:
        print(e)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO, CARD], isGroupChat = True)
def group_download_files(msg):
    """
    获取群组聊天附件内容

    Args:
        [PICTURE, RECORDING, ATTACHMENT, VIDEO, CARD]
        图片、语音、文本、视频、名片

    Demo:
        apiEg/msg_gchat_*.txt
    """
    # print(msg)
    global gchat_count, gchat_kw_count
    TODAYFOLDERPATH = create_today_folder()
    if not msg.actualNickName:
        group_one_id = "本机器人"
    else:
        group_one_id = msg['ActualNickName']    # 发送消息者ID
    group_id = msg.user['NickName']   # 聊天群组ID
    # msg['Type'] == msg.type
    file_type = msg['Type'] # 附件类型
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime']))
    file_type_symbol = {
        PICTURE: '图片',
        RECORDING: '语音',
        ATTACHMENT: '附件',
        VIDEO: '视频',
        CARD: '名片',
    }.get(msg['Type'], '未知内容')  # 附件类型标签
    gchat_count += 1

    # 文件保存
    try:
        if file_type == "Card":
            file_name = msg['Text']['NickName']
            file_dst_name = random_str(group_one_id) + '#' + file_name
            file_dst = TODAYFOLDERPATH + file_dst_name
            f = open(file_dst, 'w')
            f.write(str(msg['Text']))
            f.close()
        else:
            file_name = msg['FileName'] # 附件名字 msg.fileName
            msg.download(file_name)
            file_src = os.path.join(ROOTPATH, file_name)
            file_dst_name = random_str(group_one_id) + '#' + file_name
            file_dst = TODAYFOLDERPATH + file_dst_name
            shutil.move(file_src, file_dst)
        # res = create_time + " dlfile# " + group_id + " " + group_one_id + " " + file_type_symbol + " " + file_dst_name + " : Move Success."
        # res = str(gchat_count) + " | " + create_time + " | " + group_id + " | " + group_one_id + " | " + group_chat_text + " | " + file_type + " | " + file_name + " | " + file_dst + " | " + kw_word + " | " + kw_type + " | " + str(gchat_kw_count) + " | "
        res = dict(gchat_count = gchat_count, create_time = create_time, group_id = group_id, group_one_id = group_one_id, group_chat_text = group_chat_text, file_type = file_type, file_name = file_name, file_dst = file_dst, kw_word = kw_word, kw_type = kw_type, gchat_kw_count = gchat_kw_count)
        res = json.dumps(res, ensure_ascii=False)
        write_log_group(res + "\n")
        print(res)
    except Exception as e:
        print(e)
    
    # 插入数据，并更新参数值
    try:
        conn = sql.init()
        sql.insert_gchat(conn, create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type)
        sql.update_var(conn, gchat_count, gchat_kw_count)
        sql.finish(conn)
    except Exception as e:
        print(e)


def kw_send(msg, group_id, group_one_id, boss):
    """
    指定用户发送预警信息
    """
    msg = group_id + " # " + group_one_id + " : \n" + msg
    # 如果toUserName没有指出或为None，则发送给自己
    itchat.send(msg, toUserName = boss)
    print("kw_send Success.")


def write_log_group(msg):
    """
    群组日志记录，方便logstash处理
    """
    LOGNAME = time.strftime("%Y-%m-%d") + ".log"
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)
    LOGFILE = os.path.join(LOGPATH, LOGNAME)
    fw = codecs.open(LOGFILE, "a", "utf-8")
    fw.write(msg)
    fw.close()


def write_log_one(msg):
    """
    私聊日志记录
    """
    LOGNAME = time.strftime("%Y-%m-%d") + "-onebyone.log"
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)
    LOGFILE = os.path.join(LOGPATH, LOGNAME)
    fw = codecs.open(LOGFILE, "a", "utf-8")
    fw.write(msg)
    fw.close()


def create_today_folder():
    """
    创建FILEPATH下以当前日期命名的文件夹
    """
    TODAYFOLDERPATH = FILEPATH + time.strftime("%Y-%m-%d") + '/'
    if not os.path.exists(TODAYFOLDERPATH):
        try:
            os.makedirs(TODAYFOLDERPATH)
        except OSError as e:
            print(e)
    return TODAYFOLDERPATH


def read_msg():
    """
    获取文件内容
    """
    fw = codecs.open("file_name", "r", "utf-8", buffering = 1)
    data = fw.read()
    fw.close()


def random_str(key = string.ascii_letters, randomlength = 6):
    """
    生成随机数
    """
    str = ''
    length = len(key) - 1
    random = Random()
    for i in range(randomlength):
        str += key[random.randint(0, length)]
    return str


def main():
    """
    """
    global gchat_count, gchat_kw_count, boss
    try:
        conn = sql.init()
        (gchat_count, gchat_kw_count) = sql.select_var(conn)
        sql.finish(conn)
    except Exception as e:
        print(e)
    
    itchat.auto_login(enableCmdQR = 2)
    # itchat.auto_login(enableCmdQR = 2, hotReload = True) # 记录登陆凭证

    try:
        # kw_send boss ID
        boss = itchat.search_friends(name = "●﹏●")[0]['UserName']
        itchat.run()
    except KeyboardInterrupt as e:
        print("itchat Error ..." + e)
        itchat.logout()


if __name__ == "__main__":
    main()
