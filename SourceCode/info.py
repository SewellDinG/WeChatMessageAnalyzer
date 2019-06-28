#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Author__ = "Sewell"

'''
微信好友基本信息
'''

import itchat
from itchat.content import *
import pandas
import sql


itchat.auto_login(hotReload=True)
itchat.run()

friends = itchat.get_friends(update=True)   # 好友基本信息
print(friends)

NickName = friends[0].NickName  # 获取自己的昵称

for user in friends:
    print()
    print('user.NickName:',user.NickName)
    if user.Sex == 1:
        user_sex = "男"
        print('user.Sex:', '男')
    elif user.Sex == 2:
        user_sex = "女"
        print('user.Sex:', '女')
    else:
        user_sex = "未知"
        print('user.Sex:', '未知')
    print('user.Province:', user.Province)
    print('user.City:', user.City)
    print('user.Signature:',user.Signature)
    # 插入数据库
    try:
        conn = sql.init()
        sql.insert_friends(conn, user.NickName, user_sex, user.Province, user.City, user.Signature)
        sql.finish(conn)
    except Exception as e:
        print(e)

# 好友数量
number_of_friends = len(friends)

# pandas可以把据处理成DataFrame
df_friends = pandas.DataFrame(friends)

# 获取性别信息：男性为1、女性为2、未知为0
Sex = df_friends.Sex

# pandas为Series提供了一个value_counts()方法，可以更方便统计各项出现的次数：
Sex_count = Sex.value_counts() #defaultdict(int, {0: 31, 1: 292, 2: 245})

# Province
Province = df_friends.Province
Province_count = Province.value_counts()
Province_count = Province_count[Province_count.index!='']   # 有一些好友地理信息为空，过滤掉这一部分人。

# City
City = df_friends.City #[(df_friends.Province=='北京') | (df_friends.Province=='四川')]
City_count = City.value_counts()
City_count = City_count[City_count.index!='']

# 处理
msg_body = '测试号共有%d个好友，其中有 %d 个男生，%d 个女生，%d 未显示性别。\n\n' %(number_of_friends, Sex_count[1], Sex_count[2], Sex_count[0]) +\
           '好友主要来自省份：%s(%d)、%s(%d) 和 %s(%d)。\n\n' %(Province_count.index[0],Province_count[0],Province_count.index[1],Province_count[1],Province_count.index[2],Province_count[2]) + \
           '好友主要来自城市：%s(%d)、%s(%d)、%s(%d)、%s(%d)、%s(%d) 和 %s(%d)。'%(City_count.index[0],City_count[0],City_count.index[1],City_count[1],City_count.index[2],City_count[2],City_count.index[3],City_count[3],City_count.index[4],City_count[4],City_count.index[5],City_count[5])

print(msg_body)

# 将处理信息发送到文件助手
itchat.send_msg(msg_body, toUserName='filehelper')
