#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Author__ = "Sewell"

"""
SQLite3 数据库增删改查操作
"""

import sqlite3

ROOTPATH = "./"


def create_gchat(conn):
    """
    创建数据表:wc_gchat
    """
    try:
        sql_create = '''
            CREATE TABLE IF NOT EXISTS `wc_gchat` (
            `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
            `create_time`  TEXT NOT NULL,
            `group_id`  TEXT NOT NULL,
            `group_one_id`  TEXT NOT NULL,
            `group_chat_text`  TEXT,
            `file_type`  TEXT,
            `file_name`  TEXT,
            `file_dst`  TEXT,
            `kw_word`  TEXT,
            `kw_type`  TEXT
        )
        '''
        conn.execute(sql_create)
        print("Create Success.")
    except:
        print("Create Failed.")
        return False


def create_friends(conn):
    """
    创建数据表:wc_friends
    """
    try:
        sql_create = '''
            CREATE TABLE IF NOT EXISTS `wc_friends` (
            `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
            `name`  TEXT NOT NULL,
            `sex`  TEXT,
            `province`  TEXT,
            `city`  TEXT,
            `signature`  TEXT
        )
        '''
        conn.execute(sql_create)
        print("Create Success.")
    except:
        print("Create Failed.")
        return False


def create_var(conn):
    """
    创建数据表:wc_var
    """
    try:
        sql_create = '''
            CREATE TABLE IF NOT EXISTS `wc_var` (
            `gchat_count`  INTEGER NOT NULL,
            `gchat_kw_count`  INTEGER NOT NULL
        )
        '''
        conn.execute(sql_create)
        print("Create Success.")
    except:
        print("Create Failed.")
        return False


def insert_gchat(conn, create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type):
    """
    插入数据:wc_gchat
    """
    sql_insert = '''
    INSERT INTO
        wc_gchat(create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    # 防止SQL注入，禁止使用format传参，使用 ?
    # execute方法的参数要求是tuplp
    conn.execute(sql_insert, (create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type))
    print("Insert Success.")


def insert_friends(conn, name, sex, province, city, signature):
    """
    插入数据:wc_friends
    """
    sql_insert = '''
    INSERT INTO
        wc_friends(name, sex, province, city, signature)
    VALUES
        (?, ?, ?, ?, ?);
    '''
    conn.execute(sql_insert, (name, sex, province, city, signature))
    print("Insert Success.")


def select_var(conn):
    """
    查询数据
    """
    sql = '''
    SELECT
        `gchat_count`,
        `gchat_kw_count`
    FROM
        `wc_var`;
    '''
    data = conn.execute(sql)
    for row in data:
        gchat_count = row[0]
        gchat_kw_count = row[1]
    print("Select Success.")
    return (gchat_count, gchat_kw_count)


def delete(conn, user_id):
    """
    删除数据
    """
    sql_delte = '''
    DELETE FROM
        wc_gchat_txt
    WHERE
        id=?
    '''
    conn.execute(sql_delte, (user_id,))
    print("Delete Success.")


def update_var(conn, gchat_count, gchat_kw_count):
    """
    """
    sql_update = '''
    UPDATE
        `wc_var`
    SET
        `gchat_count`=?,
        `gchat_kw_count`=?
    '''
    conn.execute(sql_update, (gchat_count, gchat_kw_count))
    print("Update Success.")


def init():
    db_path = ROOTPATH + "db.sqlite3"
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    print("Conn Success.")
    return conn


def finish(conn):
    conn.commit()
    conn.close()


def main():
    conn = init()
    # create_gchat(conn)
    # create_friends(conn)
    # create_var(conn)
    finish(conn)


if __name__ == '__main__':
    main()
