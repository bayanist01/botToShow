# -*- coding: utf-8 -*-
import json

import config
import functions as bf
import database
from funclist import Funclist


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class SetEvent:
    keywords = ['событие', 'создай']
    commands = ['создай событие', 'событие']
    attachment = []
    help_name = 'Создай событие'
    help_content = 'бот создает событие'
    help_deep = 'Этот функционал только для бесед\n' \
                'Бот создаст событие для беседы, можно будет отмечаться кто идет, кто возможно идет, кто не идет' \
                '\nВ беседе может быть только одно событие' \
                '\nИспользование: "бот создай событие (любое название)"'

    def answer(self, message, vk, *rest):
        answer = ''
        if message.peer_id < config.vk_groupchats_id_limit:
            answer = 'Этот функционал только для бесед\n'
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        if not msg:
            answer += 'Бот создаст событие для беседы, можно будет отмечаться кто идет, кто возможно идет, кто не идет' \
                      '\nВ беседе может быть только одно событие' \
                      '\nПользоваться: бот создай "событие игра в кс" (или любое другое название)'
        if database.ForAllDataBase.getbyunique(message.peer_id, 'event'):
            update = True
        else:
            update = False
        if not answer:
            user_event = {'name': msg, 'go': [], 'maybego': [], 'dontgo': []}
            if update:
                database.ForAllDataBase.update(message.peer_id, 'event', json.dumps(user_event))
            else:
                database.ForAllDataBase.add(message.peer_id, 'event', json.dumps(user_event))
            answer = f'Событие "{msg}" создано, рекомендую воспользоваться командой "напомни" чтобы не забыть. ' \
                     f'Можно отмечаться кто идет, кто возможно идет, кто не идет' \
                     '\nВ беседе может быть только одно событие\n' \
                     'Подробности - "команда я иду" "команда кто идёт" '
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class ShowEvent:
    keywords = ['кто', 'идет', 'идёт']
    commands = ['кто идёт', 'кто идет']
    attachment = []
    help_name = 'Кто идёт'
    help_content = 'бот расскажет про событие'
    help_deep = 'Эта функция только для бесед. ' \
                'Бот выводит список всех кто отметился в событии. А так же их решение и название события\n' \
                'Использование: "бот кто идёт" или "бот кто идет"'

    def answer(self, message, vk, *rest):
        answer = ''
        if message.peer_id < config.vk_groupchats_id_limit:
            answer = 'Этот функционал только для бесед\n'
        else:
            if not database.ForAllDataBase.getbyunique(message.peer_id, 'event'):
                answer = 'Вы не создали событие'
            else:
                # user_event = {'name': msg, 'go': [], 'maybego': [], 'dontgo': []}
                user_event = json.loads(database.ForAllDataBase.getbyunique(message.peer_id, 'event'))

                answer = f'Событие \'{user_event["name"]}\':\n'
                if user_event['go']:
                    answer += 'Идут:\n'
                    for x in user_event['go']:
                        answer += f' + [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

                if user_event['maybego']:
                    answer += 'Возможно идут:\n'
                    for x in user_event['maybego']:
                        answer += f' ~ [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

                if user_event['dontgo']:
                    answer += 'Не идут:\n'
                    for x in user_event['dontgo']:
                        answer += f' - [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

                if answer == f'Событие \'{user_event["name"]}\':\n':
                    answer += 'На это событие пока ещё никто не отметился. Можешь стать первым! '

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message, disable_mentions=1)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class MarkInEvent:
    keywords = ['иду', 'не', 'возможно', 'пойду']
    commands = ['иду', 'не иду', 'возможно иду', 'возможно пойду', 'пойду', 'не пойду']
    attachment = []
    help_name = 'Я (не/возможно) иду'
    help_content = 'отметиться в событии'
    help_deep = 'Эта функция только для бесед. Бот запишет вас в нужную категорию.\n' \
                'Использование: "бот я иду", "бот я пойду", "бот я не иду", ' \
                '"бот я не пойду", "бот я возможно иду", "бот возможно пойду"'

    def answer(self, message, vk, *rest):
        if message.peer_id < config.vk_groupchats_id_limit:
            answer = 'Этот функционал только для бесед\n'

        else:
            if not database.ForAllDataBase.getbyunique(message.peer_id, 'event'):
                answer = 'Вы не создали событие'

            else:
                # user_event = {'name': msg, 'go': [], 'maybego': [], 'dontgo': []}
                user_event = json.loads(database.ForAllDataBase.getbyunique(message.peer_id, 'event'))
                msg = message.text.lower()

                for key in user_event:
                    if key != 'name':
                        for x in user_event[key]:
                            if x == message.from_id:
                                user_event[key].remove(x)

                if 'возможно' in msg:
                    user_event['maybego'].append(message.from_id)
                    answer = 'Отметил тебя как "возможно идёт"'

                elif 'не' in msg:
                    user_event['dontgo'].append(message.from_id)
                    answer = 'Отметил тебя как "не идёт"'

                else:
                    user_event['go'].append(message.from_id)
                    answer = 'Отметил тебя как "идёт"'

                database.ForAllDataBase.update(message.peer_id, 'event', json.dumps(user_event))
                answer += f'\nСобытие \'{user_event["name"]}\':\n'

                if user_event['go']:
                    answer += 'Идут:\n'
                    for x in user_event['go']:
                        answer += f' + [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

                if user_event['maybego']:
                    answer += 'Возможно идут:\n'
                    for x in user_event['maybego']:
                        answer += f' ~ [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

                if user_event['dontgo']:
                    answer += 'Не идут:\n'
                    for x in user_event['dontgo']:
                        answer += f' - [id{x}|{vk.users.get(user_ids=x)[0].get("first_name")}] \n'

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message, disable_mentions=1)

