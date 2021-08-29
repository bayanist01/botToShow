# -*- coding: utf-8 -*-
import json

import functions as bf
import database
import config
from funclist import Funclist

# TODO убедиться что тут собраны все инструкции каждого функлиста


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Instruction:
    commands = ['помощь', 'хелп', 'инструкция', 'инструкции', 'команды', 'help', 'справка']
    keywords = commands
    attachment = []
    help_name = 'Помощь'
    help_content = 'выводит список команд и их предназначение'
    help_deep = 'Команда (название команды) - выведет подробную информацию о команде'

    def answer(self, message, vk, *rest):
        answer = 'Краткая справка: \n'
        admins = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))
        friends = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'friends_id'))
        if message.from_id in admins:
            answer += AdminInstructions.help_name + ' - ' + AdminInstructions.help_content
            answer += '\n'
        for f in Funclist.standartfunclist:
            answer += f.help_name + ' - ' + f.help_content
            answer += '\n'
        if message.from_id in friends or message.from_id in admins:
            answer += '\n'
            for f in Funclist.friendfunclist:
                answer += f.help_name + ' - ' + f.help_content
                answer += '\n'
        answer += '\n Для работы дополнительных команд требуется разрешение боту видеть все сообщения  в беседе, ' \
                  'а не только упоминания. Разрешение может дать администратор беседы в настройках\n '
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Command:
    commands = ['команда']
    keywords = commands
    attachment = []
    help_name = 'Команда'
    help_content = 'выводит подробную информацию о команде'
    help_deep = 'Команда (название команды) - выведет подробную информацию о команде'

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        answer = ''
        if msg:
            for fl in Funclist.searchlist:
                for f in fl:
                    fname = f.help_name.lower().strip()
                    if (fname in msg) or (set(msg.split(' ')).intersection(f.commands)):
                        answer += f'{f.help_name} - {f.help_content}\n{f.help_deep}\n\n'
        if not answer:
            answer = 'Не понял информацию о какой команде ты хочешь получить\n Попробуй "команда напомни"'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class GamesInstructions:
    commands = ['игры']
    keywords = commands
    attachment = []
    help_name = 'Игры'
    help_content = 'выводит список игр'
    help_deep = 'Команда (название игры) - подробная информация по игре'

    def answer(self, message, vk, *rest):
        answer = 'Краткая справка по играм: \n'
        for f in Funclist.gamesfunclist:
            answer += f'{f.help_name} - {f.help_content}\n'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AdminInstructions:
    commands = ['админка']
    keywords = ['админка']
    attachment = []
    help_name = 'Админка'
    help_content = 'выводит список админских команд и их предназначение'
    help_deep = 'Эти команды доступны только админам. Предполагается, что вы знаете как ими правильно пользоваться' \
                ' и не натворите глупостей. Лучше спросите или запросите подробную информацию'

    def answer(self, message, vk, *rest):
        answer = f'Админские команды: \n{self.help_deep}\n'
        for f in Funclist.adminfunclist:
            answer += f'{f.help_name} - {f.help_content}\n'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)
