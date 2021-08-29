# -*- coding: utf-8 -*-
import json
import re
from random import choice

import functions as bf
import database
import config
from funclist import Funclist


@bf.register(Funclist.silentfunclist)
@bf.addtrigger(bf.standart_trigger)
class TikTokAdd:
    keywords = ['tiktok']
    commands = keywords
    attachment = []
    help_name = 'Тикток'
    help_content = 'бот сохранит себе ссылку на тикток, увиденный в переписках'
    help_deep = 'Когда боту(или в беседке где бот видит все сообщения) ' \
                'кто-то кидает ссылку на тикток, бот ее запоминает' \
                'и может потом выдать по команде "бот тикток".\n' \
                'Использование: работает автоматически'

    def answer(self, message, vk, *rest):
        msg = message.text
        url = re.findall(r'\b\S*tiktok\S*\b', msg)
        dbtt = database.ForAllDataBase.getbyunique(config.my_id, 'tiktoks')

        if url:
            config.logger.debug(url)
            update = True if dbtt else False

            if update:
                listoftt = json.loads(dbtt)
            else:
                listoftt = []

            for x in url:
                if x.startswith('http'):
                    listoftt.append(x)

            if update:
                database.ForAllDataBase.update(config.my_id, 'tiktoks', json.dumps(listoftt))
            else:
                database.ForAllDataBase.add(config.my_id, 'tiktoks', json.dumps(listoftt))


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class DeleteTikTok:
    keywords = ['удали', 'тикток']
    commands = ['удали тикток']
    attachment = []
    help_name = 'Удали Тикток'
    help_content = 'бот cнесет базу данных тиктоков'
    help_deep = 'Сносит прям всю, частичное удаление не поддерживается.\n' \
                'Использование: "бот удали тикток" '

    def answer(self, message, vk, *rest):
        dbtt = database.ForAllDataBase.getbyunique(config.my_id, 'tiktoks')
        update = True if dbtt else False
        listoftt = []

        if update:
            database.ForAllDataBase.update(config.my_id, 'tiktoks', json.dumps(listoftt))

        else:
            database.ForAllDataBase.add(config.my_id, 'tiktoks', json.dumps(listoftt))

        bf.sendmessage(vk, peer_id=message.peer_id, answer='Удалил', mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class TikTokSend:
    keywords = ['тикток']
    commands = keywords
    attachment = []
    help_name = 'Тикток'
    help_content = 'бот скинет один из тиктоков увиденных в переписках'
    help_deep = 'Если вам попалось что-то чего тут явно быть не должно - напишите в техподдержку, мы почистим.' \
                'Если хотите пополнить базу тиктоков - кидай их друзьям при боте или сразу боту\n' \
                'Использование: "бот тикток" '

    def answer(self, message, vk, *rest):
        dbtt = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'tiktoks'))

        if dbtt:
            answer = choice(dbtt)
        else:
            answer = 'Ещё не видел ни одного тиктока, можешь накидать мне их в лс'

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)
