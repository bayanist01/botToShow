# -*- coding: utf-8 -*-
import json
from random import choice

import functions as bf
import database
import config
from funclist import Funclist
from modules.tools import MyTranslator
from texts import texts


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class Workdone:
    keywords = ['отдохни', 'выключайся', 'выключись', 'обнова']
    commands = ['отдохни', 'выключайся', 'выключись', 'обнова']
    attachment = []
    help_name = 'Отдохни'
    help_content = 'выключает бота'
    help_deep = 'Бот выключится, проверит гитхаб, если там есть что-то новое скачает, а потом запустится обратно.' \
                ' В среднем этот процесс занимает секунд 30\n' \
                'Использование: "бот отдохни", "бот выключайся", "бот выключись" или "бот обнова"'

    def answer(self, message, vk, workdone, *rest):
        answer = "Ухожу спать..."
        workdone.set()
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class GetPeer:
    keywords = ['peer', 'пир']
    commands = keywords
    attachment = []
    help_name = 'Пир'
    help_content = 'высылает пир беседы'
    help_deep = 'В личке вышлет ваше айди. В беседке - порядковый номер беседы среди диалогов бота.' \
                'Команда предназначена для задания беседы техподдержки и возможно в будущем для чата через бота\n' \
                'Использование: "бот пир" или "бот peer" или "/peer" '

    def answer(self, message, vk, *rest):
        answer = message.peer_id
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class SetSupportPeer:
    keywords = ['пир', 'задай']
    commands = ['задай пир']
    attachment = []
    help_name = 'Задай пир'
    help_content = 'задает пир техподдержки'
    help_deep = 'Теперь команда бот техподдержка начнет пересылать сообщения в указанную беседку. ' \
                'Получить пир текущей беседки можно по команде "бот пир" \n' \
                'Использование: "бот задай пир 2000000001"'

    def answer(self, message, vk, *rest):
        admins = [int(x) for x in json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))]
        if message.from_id in admins:
            msg = bf.erase_command(message.text, self.commands)
            peer = int(msg.strip())
            database.ForAllDataBase.update(config.my_id, 'support', json.dumps(peer))
            bf.sendmessage(vk, peer_id=message.peer_id, answer='Задал')


@bf.register(Funclist.emptyfunclist)
@bf.addtrigger(bf.just_in_trigger)
class EmptyMessage:
    keywords = ['']
    commands = ['']
    attachment = []
    help_name = 'Бот'
    help_content = 'Проверка активности бота или бот не понял чего от него хотят'
    help_deep = 'Функция ответа на команду для бота которой бот не знает'

    def answer(self, message, vk, *rest):
        for x in message.text.lower():
            if x in 'qwertyuiopasdfghjklzxcvbnm':
                MyTranslator.answer(message, vk)
                return
        answer = choice(texts.wuw)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class GetFuncStat:
    keywords = ['статистика']
    commands = keywords
    attachment = []
    help_name = 'Статистика'
    help_content = 'бот скидывает частоту использования команд'
    help_deep = 'Это все вызовы команд. Честно посчитанные.\n' \
                'Если дописать айди выдаст всю информацию которая у него есть на этот айди\n' \
                'Использование: "бот статистика" или "бот статистика 21354688"'

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        id = None
        answer = ''
        if msg:
            for x in msg.split(' '):
                if x.isdigit():
                    id = int(x)
            if id:
                db = database.ForAllDataBase.getbyid(id)
                if db:
                    answer += f'Статистика id{id}:\n'
                    for x in db:
                        answer += f'{x[1]} - {x[2]}\n'
        else:
            stats = database.FuncStatDataBase.getall()
            stats.sort(key=(lambda x: x[1]), reverse=True)
            for i in stats:
                answer += 'Функция ' + i[0] + ' вызывалась ' + str(i[1]) + ' раз\n'
        if not answer:
            answer = 'Статистика пуста'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)
