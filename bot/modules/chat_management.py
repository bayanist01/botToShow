# -*- coding: utf-8 -*-

import functions as bf
from funclist import Funclist
import database
import config


@bf.register(Funclist.friendfunclist)
@bf.addtrigger(bf.standart_trigger)
class Fork:
    keywords = ['форк']
    commands = keywords
    attachment = []
    help_name = 'Форк'
    help_content = 'создать беседу и скинуть ссылку-приглашение в лс всем перечисленным юзерам'
    help_deep = 'Использование:"бот форк", "бот форк 12345678" или "бот форк *user *user2" '

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        numbers = []

        if msg:
            num_msg = msg
            for x in msg:
                if not x.isdigit():
                    num_msg = num_msg.replace(x, ' ')
            numbers.extend([int(x) for x in num_msg.split(' ') if x.isdigit()])

        numbers.append(message.from_id)
        chat_id = vk.messages.createChat(user_ids=numbers, title='Беседа - новое лс')
        link = vk.messages.getInviteLink(peer_id=config.vk_groupchats_id_limit + chat_id, reset=1, group_id=config.my_id)
        invite = link['link']
        title = database.ForAllDataBase.getbyunique(message.from_id, 'title')
        cantsend = []

        for x in numbers:
            if vk.messages.isMessagesFromGroupAllowed(group_id=config.my_id, user_id=x)['is_allowed']:
                bf.sendmessage(vk, peer_id=x,
                               answer=f'[id{message.from_id}|'
                                      f'{title.capitalize() if title else vk.users.get(user_ids=x)[0].get("first_name")}]'
                                      f' приглашает вас в беседу: {invite}')
            else:
                cantsend.append(x)
        if cantsend:
            answer = ''
            for x in cantsend:
                answer += f'[id{x}|{vk.users.get(user_ids=x, name_case="dat")[0].get("first_name")}] '
            bf.sendmessage(vk, peer_id=message.peer_id,
                           answer=f'{answer} прислать не смог. Мне не разрешали присылать сообщения')
