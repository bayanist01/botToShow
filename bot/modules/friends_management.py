# -*- coding: utf-8 -*-
import json

import functions as bf
import database as database
import config as config
from funclist import Funclist


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class SetFriend:
    keywords = ['друг']
    commands = keywords
    attachment = []
    help_name = 'Друг'
    help_content = 'Изменить статус друга для пользователя'
    help_deep = 'Использование: "бот 182882773 друг" или "бот *user не друг" '

    def answer(self, message, vk, *rest):
        db = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'friends_id'))
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        answer = ''

        if not msg:
            answer = self.help_deep

        else:
            num_msg = msg

            for x in msg:
                if not x.isdigit():
                    num_msg = num_msg.replace(x, ' ')

            numbers = [int(x) for x in num_msg.split(' ') if x.isdigit()]

            if not numbers:
                answer = self.help_deep

            else:
                id_ = numbers[0]
                if 'не' in msg:
                    if id_ in db:
                        db.remove(id_)
                else:
                    if id_ not in db:
                        db.append(id_)

        if db:
            database.ForAllDataBase.update(config.my_id, 'friends_id', json.dumps(db))
        if not answer:
            answer = f'{id_} обновлен. Друзья: {json.dumps(db)}'

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


