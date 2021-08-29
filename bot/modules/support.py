# -*- coding: utf-8 -*-
import json

import functions as bf
import database
import config
from funclist import Funclist


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AdminAnswer:
    keywords = ['ответь']
    commands = ['ответь']
    attachment = []
    help_name = 'Ответь {id}'
    help_content = 'шлет админское текстовое сообщение по айди'
    help_deep = 'Получатель получит сообщение вида "Техподдерка: *ТУТВАШТЕКСТ*". ' \
                'Можно ответить не указывая айди человека, если отвечать на сообщение бота с запросом техподдержки\n' \
                'Использование: "бот ответь 123456789 я не брал твою гречу" ' \
                'или "бот ответь сам дурак"(если ответил на сообщение бота)'

    def answer(self, message, vk, *rest):
        admins = [int(x) for x in json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))]
        if message.from_id in admins:
            answer = ''

            msg = bf.erase_command(message.text, self.commands)
            msg = msg.replace('\n', ' ').strip()

            msg_splitted = msg.split(' ', 1)
            peer = msg_splitted.pop(0)

            if msg_splitted:
                answer = msg_splitted.pop(0)
            peer = peer.strip()

            if peer.isdigit():
                peer = int(peer)
            else:
                if message.fwd_messages:
                    for i in message.get('fwd_messages'):
                        txt = i.get('text')
                        if 'Запрашивают техподдержку из' in txt:
                            peer = int(txt.split(' ')[-1])
                else:
                    peer = config.creator_id
                answer = msg
            if answer:
                answer = 'Техподдержка: ' + answer
                bf.sendmessage(vk, peer_id=peer, answer=answer)
                bf.sendmessage(vk, peer_id=message.peer_id, answer='Ответил')
            else:
                bf.sendmessage(vk, peer_id=message.peer_id, answer='А чё ответить то?')


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class TechSup:
    keywords = ['техподдержка']
    commands = keywords
    attachment = []
    help_name = 'Техподдержка'
    help_content = 'перешлет сообщение с описанием проблемы админам'
    help_deep = 'Если у вас что-то случилось или бот работает не так как вы того ожидали,' \
                ' можете попросить помощи техподдержки\n' \
                'Использование: "бот техподдержка у меня все сломалось"'

    def answer(self, message, vk, *rest):
        if message.peer_id > config.vk_groupchats_id_limit:
            answer = 'Боты не могут пересылать сообщения из беседок. Напиши в лс'

        else:
            answer = 'Отправил, с вами свяжутся'
            support_peer = json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'support'))
            bf.sendmessage(vk, peer_id=support_peer,
                           answer='Запрашивают техподдержку из ' + str(message.peer_id),
                           fwd_messages=message.id)

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)
