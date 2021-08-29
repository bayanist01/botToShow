# -*- coding: utf-8 -*-
import time
import requests

import functions as bf
from funclist import Funclist


@bf.register(Funclist.friendfunclist)
@bf.addtrigger(bf.standart_trigger)
class MCServer:
    keywords = ['сервер', 'серв']
    commands = keywords
    attachment = []
    help_name = 'Сервер'
    help_content = 'Выдаст никнеймы игроков которые сейчас находятся на сервере майнкрафта yc.mickle.me'
    help_deep = 'Использование:"бот сервер", "бот серв" или "/серв" '

    def answer(self, message, vk, *rest):
        re = requests.get('https://mcapi.us/server/status?ip=yc.mickle.me&port=25565')
        names = re.json()['players']['sample']
        if (time.time() - int(re.json()['last_online']) > 100) or not names:
            ans = 'Сервер пуст :('
        else:
            ans = 'Сейчас на сервере: \n'
            ans += '\n'.join(f'{i}) {x["name"]}' for i, x in enumerate(names, 1))
        bf.sendmessage(vk, peer_id=message.peer_id, answer=ans)
