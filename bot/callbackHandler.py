# -*- coding: utf-8 -*-

from random import choice

import database
import functions
import config


def find_handler(vk, event):
    """Функция выбирает по пэйлоаду которой функции-обработчику его передать

    :param vk: апи
    :param event: апи-ивент (событие нажатия на кнопочку
    :return: None
    """
    if event.object.payload in ['0', 1, 2]:
        rps_handler(vk, event)


# камень - 0, ножницы - 1, бумага - 2
# функция вычисления победителя
def rpswinner(first, second):
    if first == second:
        return None
    if (int(first) - int(second)) % 3 == 1:
        return second
    else:
        return first


def get_mention(user_id, vk, name_case='nom'):
    user_name = vk.users.get(user_ids=user_id, name_case=name_case)[0].get('first_name')
    return f'[id{user_id}|{user_name}]'


def rps_handler(vk, event):
    """Функция решает что делать с информацией о нажатии кнопки в игре камень ножницы бумага
    запоминает первого ответившего
    второму ответившему присылает результат состязания с первым

    :param vk: api
    :param event: api event
    :return: None
    """
    peer = event.object.peer_id
    message = ''
    if peer < config.vk_groupchats_id_limit:
        message = choice(['Я победил!', 'Ты победил!', 'Ничья'])
    else:
        res = database.RPSDataBase.get(peer)
        if res:
            res = res[0]
            if res.user_id != event.object.user_id:
                winner = rpswinner(event.object.payload, res.rps)

                if winner:

                    if winner == res.rps:
                        winner_id = res.user_id
                        loser_id = event.object.user_id
                    else:
                        winner_id = event.object.user_id
                        loser_id = res.user_id

                    winner_sex = vk.users.get(user_ids=winner_id, fields='sex')[0].get('sex')
                    message = f'{get_mention(winner_id, vk)} победил{"а" if winner_sex == 1 else ""} ' \
                              f'{get_mention(loser_id, vk, "acc")}!'

                else:
                    message = f'Ничья!\nМежду {get_mention(res[1],vk, "ins")} и ' \
                              f'{get_mention(event.object.user_id, vk, "ins")}'
            else:
                database.RPSDataBase.add([res.peer, res.user_id, res.rps])
        else:
            database.RPSDataBase.add([event.object.peer_id, event.object.user_id, event.object.payload])
            functions.sendmessage(vk, peer_id=peer, answer=f'{get_mention(event.object.user_id, vk)} '
                                                           f'определился с ходом, кто даст ему бой?')

    if message:
        functions.sendmessage(vk, peer_id=peer, answer=message)
