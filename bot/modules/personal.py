# -*- coding: utf-8 -*-

import functions as bf
import database as database
from funclist import Funclist


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class GetMyLevel:
    keywords = ['уровень']
    commands = keywords
    attachment = []
    help_name = 'Уровень'
    help_content = 'узнать свой уровень в боте'
    help_deep = 'Уровень вычисляется на основании того как часто вы пользуетесь ботом \n' \
                'Использование: "бот уровень" или "бот мой уровень" '

    def answer(self, message, vk, *rest):
        if message.from_id > 0:
            db = database.ForAllDataBase.getbyunique(message.from_id, 'level')
            if db:
                answer = f'Твой уровень - {int(db)}'
            else:
                answer = f'Твой уровень - 0'
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.friendfunclist)
@bf.addtrigger(bf.standart_trigger)
class Rename:
    keywords = ['называй', 'меня']
    commands = ['называй меня']
    attachment = []
    help_name = 'Называй меня'
    help_content = 'бот меняет обращение'
    help_deep = 'Хотите чтобы бот обращался к вам как-то по особому? Вам сюда!\n' \
                'Использование: "бот называй меня Обжора"'

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        answer = ''
        if not msg:
            answer = 'Ты не сказал как называть'

        update = database.ForAllDataBase.getbyunique(message.from_id, 'title')

        if not answer:
            if update:
                database.ForAllDataBase.update(message.from_id, 'title', msg)
            else:
                database.ForAllDataBase.add(message.from_id, 'title', msg)
            answer = 'Хорошо, да будет так'

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)

