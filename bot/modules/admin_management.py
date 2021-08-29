# -*- coding: utf-8 -*-

import json

import functions as bf
from funclist import Funclist
import database
import config


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AddAdmin:
    commands = ['добавь админа', 'добавь в админы']
    keywords = ['добавь', 'админы', 'админа']
    attachment = []
    help_name = 'Добавь админа {id}'
    help_content = 'добавляет юзера по айди в админы'
    help_deep = 'Ему станут доступны ВСЕ команды из Админки. ' \
                'Захардкоженый админ бота получит оповещение в личку о вызове этой команды\n' \
                'Использование: "бот добавь админа 19248300" или "бот добавь в админы 122313"'

    def answer(self, message, vk, *args):
        admins = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))
        if message.from_id in [int(x) for x in admins]:
            msg = bf.erase_command(message.text, self.commands)
            id_ = int(msg.strip())
            admins.append(id_)
            database.ForAllDataBase.update(config.my_id, 'admin_id', json.dumps(admins))

            answer = 'Добавил'
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)

            answer = f'[id{id_}|Этот чел] ({id_}) был добавлен в админы [id{message.from_id}|этим челом] ' \
                     f'({message.from_id})'
            bf.sendmessage(vk, peer_id=config.creator_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class DelAdmin:
    commands = ['удали админа', 'удали из админов']
    keywords = ['удали', 'админа', 'админов']
    attachment = []
    help = ' - '
    help_name = 'Удали админа {id}'
    help_content = 'удаляет юзера по айди из админов'
    help_deep = 'Захардкоженого удалить нельзя. Ему придет уведомление о том, что вы кого-то удалили\n' \
                'Использование: "бот удали админа 19248300" или "бот удали из админов 122313"'

    def answer(self, message, vk, *rest):
        admins = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))

        if message.from_id in [int(x) for x in admins]:
            msg = bf.erase_command(message.text, self.commands)
            id_ = int(msg.strip())

            if id_ == config.creator_id:
                bf.sendmessage(vk, peer_id=config.creator_id,
                               answer=f'Тебя пытался удалить из админов [id{message.from_id}|Этот чел] '
                                      f'({message.from_id})')
                bf.sendmessage(vk, peer_id=message.peer_id, answer='Ошибка')
                return

            admins.remove(id_)
            database.ForAllDataBase.update(config.my_id, 'admin_id', json.dumps(admins))
            bf.sendmessage(vk, peer_id=message.peer_id, answer='Удалил')
            answer = f'[id{id_}|Этот чел] ({id_}) был удален из админов [id{message.from_id}|этим челом] ' \
                     f'({message.from_id})'

            bf.sendmessage(vk, peer_id=config.creator_id, answer=answer)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AllAdmin:
    commands = ['список админов', 'все админы']
    keywords = ['список', 'админов', 'админы', 'все']
    attachment = []
    help = 'Все админы - выводит список админов'
    help_name = 'Все админы'
    help_content = 'выводит список админов'
    help_deep = 'Только айдишники, дальше уже сами ищите\n' \
                'Использование: "бот все админы" или "бот список админов"'

    def answer(self, message, vk, *rest):
        admins = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))
        if message.from_id in [int(x) for x in admins]:
            answer = ", ".join([str(a) for a in admins])

            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)
