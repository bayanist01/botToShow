# -*- coding: utf-8 -*-

import sqlite3
import threading
import json
import contextlib
from collections.abc import Iterable
from dataclasses import dataclass

import config


@dataclass
class Remind:
    time: int
    user_id: int
    peer_id: int
    message_id: int
    message_text: str
    to_me: int


@dataclass
class RpsResult:
    peer: int
    user_id: int
    rps: int


def init_databases():
    ReminderDataBase.createtable()
    RPSDataBase.createtable()
    DDosDataBase.createtable()
    FuncStatDataBase.createtable()
    ForAllDataBase.createtable()

    # set admins_id
    if not ForAllDataBase.getbyunique(config.my_id, 'admin_id'):
        admin_id = [config.creator_id]
        ForAllDataBase.add(config.my_id, 'admin_id', json.dumps(admin_id))

    # set friends_id
    if not ForAllDataBase.getbyunique(config.my_id, 'friends_id'):
        friends_id = []
        ForAllDataBase.add(config.my_id, 'friends_id', json.dumps(friends_id))

    # set support_id
    if not ForAllDataBase.getbyunique(config.my_id, 'support'):
        support = config.creator_id
        ForAllDataBase.add(config.my_id, 'support', json.dumps(support))


class FuncStatDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS funcstat
                                   (funcname text, count integer) ''')

    @classmethod
    def increase(cls, string):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM funcstat WHERE funcname=?', [string])
                    reslist = cursor.fetchall()
                    if reslist:
                        cursor.execute('UPDATE funcstat SET count = count + 1 WHERE funcname=?', [string])
                    else:
                        reslist = [string, 1]
                        cursor.execute('INSERT INTO funcstat VALUES (?,?)', reslist)

    @classmethod
    def getall(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM funcstat')
                    reslist = cursor.fetchall()
        return reslist


class DDosDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        cls.lock = threading.Lock()
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS ddos
                                          (id INTEGER PRIMARY KEY AUTOINCREMENT, audio text, strings text) ''')

    @classmethod
    def add(cls, values: list):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('INSERT INTO ddos (audio, strings) VALUES (?,?)', values)

    @classmethod
    def get(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM ddos ORDER BY random() LIMIT 1')
                    reslist = cursor.fetchone()
                    if reslist:
                        reslist = list(reslist)[1:]
        return reslist

    @classmethod
    def getall(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM ddos')
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def delete(cls, id_):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('DELETE FROM ddos WHERE id=?', [id_])

    @classmethod
    def getcur(cls, id_):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM ddos WHERE id=?', [id_])
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def updatecur(cls, id_, ddos):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/ddosdatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('UPDATE ddos SET audio = ?, strings = ? WHERE id = ?', (*ddos, id_))


class ForAllDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS alldb
                                      (id integer, name text, content text, CONSTRAINT unq UNIQUE (id, name)) ''')

    @classmethod
    def add(cls, id_, name, content):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('INSERT INTO alldb VALUES (?,?,?)', (int(id_), name, content))

    @classmethod
    def update(cls, id_, name, content):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('UPDATE alldb SET content = ? WHERE (id = ? AND name = ?)', (content, id_, name))

    @classmethod
    def getall(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM alldb')
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def getbyid(cls, id_):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM alldb WHERE id=?', [id_])
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def getbydate(cls, name, today):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT id FROM alldb WHERE ( name=? AND content LIKE ? ) ', [name, today])
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def getbyunique(cls, id_, name):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/foralldatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT content FROM alldb WHERE (id=? AND name=?)', (id_, name))
                    reslist = cursor.fetchone()
        return reslist[0] if reslist else reslist


class RPSDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS rps
                                      (peer integer, userid integer, rps integer) ''')

    @classmethod
    def add(cls, list_: list):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('INSERT INTO rps VALUES (?,?,?)', list_)

    @classmethod
    def get(cls, peer: int):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM rps WHERE peer=?', [peer])
                    reslist = cursor.fetchall()
                    cursor.execute('DELETE FROM rps WHERE peer=?', [peer])

        if reslist and isinstance(reslist[0], Iterable):
            return [RpsResult(*x) for x in reslist]

        elif reslist:
            return [RpsResult(*reslist)]

        return reslist


class ReminderDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                                          (time integer, userid integer, peerid integer,
                                           messageid integer, messagetext text, tome integer) ''')

    @classmethod
    def addremind(cls, remindlist: list):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('INSERT INTO reminders VALUES (?,?,?,?,?,?)', remindlist)

    @classmethod
    def getremind(cls, now: int):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect('db/mydatabase.db', check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM reminders WHERE time<?', [now])
                    reslist = cursor.fetchall()
                    cursor.execute('DELETE FROM reminders WHERE time<?', [now])

        if reslist and isinstance(reslist[0], Iterable):
            reminds = []
            for r in reslist:
                reminds.append(Remind(*r))

        elif reslist:
            reminds = [Remind(*reslist)]

        else:
            reminds = []

        return reminds
