# -*- coding: utf-8 -*-

from vk_api.utils import get_random_id
import json
import re
import math

import config
import database
from texts import texts


def anti_troll(s):
    """Заменяет 'я' на 'ты' и так далее, чтобы бот не смог случайно обозвать себя"""
    for key in texts.atroll:
        if key in s.lower():
            s = re.sub(rf'\b{key}\b', texts.atroll[key], s, flags=re.IGNORECASE)
    return s


def erase_mention(method_to_decorate):
    """убирает всякие "/" и "бот" """

    def wrapper(message, *args):
        inputmsg = message.text.strip()

        inputmsg = re.sub(rf'\[club{config.my_id}\|(.*?)]', '', inputmsg)
        inputmsg = re.sub(r'^[/ \s]*', '', inputmsg)
        inputmsg = re.sub(r'^(,jn|<jn|бот| )*', '', inputmsg, flags=re.IGNORECASE)

        message.text = inputmsg
        return method_to_decorate(message, *args)

    return wrapper


def erase_command(text, listofcommands):
    """убирает самую левую команду из входящего сообщения"""
    answer_ = text
    low = answer_.lower()
    startcom = len(low)
    stopcom = startcom
    for x in listofcommands:
        if low.find(x) > -1:
            if low.find(x) < startcom:
                startcom = low.find(x)
                stopcom = startcom + len(x)
    answer_ = answer_[:startcom] + answer_[stopcom:]
    return answer_


def get_group_members(group_name):
    return [int(x) for x in json.loads(database.ForAllDataBase.getbyunique(config.my_id, group_name))]


@erase_mention
def answer(message, tome, vk, workdone, Funclist):
    """Основная функция, ищет что ответить на сообщение

    :param message:  сообщение
    :param tome: мне или мимо пролетало
    :param vk: апи
    :param workdone: флаг который нужно будет поднять функции чтобы бот умер
    :param Funclist: список доступных команд
    :return: ничего
    """
    # массив под команды в которых есть что-то похожее на вызов
    # funclist
    triggered_funcs = []
    # funclists list
    funclists = []

    if tome:
        if message.from_id in get_group_members('admin_id'):
            funclists = [Funclist.adminfunclist, Funclist.friendfunclist]
        elif message.from_id in get_group_members('friends_id'):
            funclists += [Funclist.friendfunclist]
        funclists += [Funclist.standartfunclist,
                      Funclist.gamesfunclist,
                      Funclist.silentfunclist,
                      Funclist.emptyfunclist]
    else:
        funclists.append(Funclist.silentfunclist)

    for funclist in funclists:
        for function in funclist:
            trig = function.trigger(message)
            if trig is not None:
                triggered_funcs.append([trig, function])
        if triggered_funcs:
            # выбираем функцию и отвечаем
            triggered_funcs.sort(key=(lambda x: x[0]))
            curfunc = triggered_funcs[0][1]
            curfunc.answer(message, vk, workdone)

            # занимательная статистика
            update_statistics(curfunc, message.from_id, vk)
            return


def update_statistics(curfunc, user_id, api):
    classname = curfunc.__class__.__name__
    database.FuncStatDataBase.increase(classname)

    if user_id and user_id > 0:

        # подсчет сколько раз пользователь вызывал эту команду
        update = database.ForAllDataBase.getbyunique(user_id, classname + '_stat')
        if update:
            counter = int(update) + 1
            database.ForAllDataBase.update(user_id, classname + '_stat', str(counter))
        else:
            database.ForAllDataBase.add(user_id, classname + '_stat', str(1))

        # подсчет сколько раз пользователь использовал бота
        update = database.ForAllDataBase.getbyunique(user_id, 'botwasused')
        if update:
            counter = int(update) + 1
            database.ForAllDataBase.update(user_id, 'botwasused', str(counter))

            level = int(math.log(counter, 2))
            oldlevel = database.ForAllDataBase.getbyunique(user_id, 'level')
            if oldlevel:
                if int(oldlevel) != level:
                    database.ForAllDataBase.update(user_id, 'level', str(level))
                    if level > 8:
                        sendmessage(api, peer_id=config.creator_id,
                                    answer=f'id {user_id} достиг уровня {level}')

                    # получаем др пользователя каждые 2^n использований бота
                    note_user_bdate(user_id, api)
            else:
                database.ForAllDataBase.add(user_id, 'level', level)

        else:
            database.ForAllDataBase.add(user_id, 'botwasused', str(1))


def note_user_bdate(user_id, api):
    user_info = api.users.get(user_ids=user_id, fields='bdate')[0]
    user_bdate = user_info.get('bdate', '') + '.'

    db_info = database.ForAllDataBase.getbyunique(user_id, 'bdate')
    update = True if db_info else False

    if user_bdate != db_info:
        if update:
            database.ForAllDataBase.update(user_id, 'bdate', user_bdate)
        else:
            database.ForAllDataBase.add(user_id, 'bdate', user_bdate)


'''
Триггеры - функции внутри класса команды которые возвращают None если сообщение не вызывает команду,
 и вхождение команды в сообщение
или необходимость ее выполнения, если команда должна сработать в ответ на сообщение
'''


def standart_trigger(self, message):
    """удаляет все небуквы из сообщения и проверяет на пересечение лист слов триггеров и слова сообщения
    если нашлись находит самое левое вхождение команды в сообщение и возвращает его позицию в строке

    :param self: класс команды
    :param message: vk message
    :return: int or None
    """
    msg = message.text.lower()
    trigger = None
    replaces = {x for x in msg if not x.isalnum()}
    for x in replaces:
        msg = msg.replace(x, ' ')
    while '  ' in msg:
        msg = msg.replace('  ', ' ')
    if set(self.keywords).intersection(msg.split(' ')):
        for x in self.commands:
            t = msg.find(x)
            if t != -1:
                if trigger:
                    trigger = min(t, trigger)
                else:
                    trigger = t
    return trigger


def attachment_trigger(self, message):
    """проверяет содержит ли сообщение вложение необходимого для команды типа. Будь то изображение или стикер

    :param self: класс команды
    :param message: сообщение вк
    :return: None or True
    """
    if message.attachments:
        for m in message.attachments:
            if m['type'] in self.attachment:
                return True


def just_in_trigger(self, message):
    """Проверяет вошла ли хоть одна команда из команды в сообщение и возвращает первое вхождение которое найдет
    Хорошо сработает для команды которая должна среагировать на '?' хоть гденибудь в сообщении """
    for i in self.commands:
        if i in message.text.lower():
            return message.text.lower().find(i)


def addtrigger(func):
    """Прикручивает вышеперечисленные триггеры к классам команд """
    def wrap(cls):
        cls.trigger = func
        return cls
    return wrap


def sendmessage(vk, **rest):
    mesfromuser = rest.get('mesfromuser', None)

    answer_ = rest.get('answer', '')

    if mesfromuser:
        if mesfromuser.from_id > 0:
            title = database.ForAllDataBase.getbyunique(mesfromuser.from_id, 'title')

            if not title:
                title = vk.users.get(user_ids=mesfromuser.from_id)[0].get('first_name')

            answer_ = f"{title.capitalize()}, {answer_}"

            if not vk.groups.isMember(group_id=config.my_id, user_id=mesfromuser.from_id):
                answer_ += '\nЭта строка пропадет, если подписаться:)'

    kk = json.dumps(rest.get('keyboard', ''))

    try:
        vk.messages.send(
            peer_id=rest.get('peer_id'),
            random_id=get_random_id(),
            message=answer_,
            attachment=rest.get('attachment', ''),
            sticker_id=rest.get('sticker_id', ''),
            keyboard=kk,
            forward_messages=rest.get('fwd_messages', ''),
            disable_mentions=rest.get('disable_mentions', 0)
        )
    except Exception as e:
        config.logger.exception(e)
        if config.debug:
            raise


def register(funclist_):
    """Прикручивает классы команд к спискам функций"""
    def wrap(cls):
        funclist_.append(cls())
        return cls
    return wrap
