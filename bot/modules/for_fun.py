# -*- coding: utf-8 -*-
import json
import threading
from hashlib import md5
from random import choice
import requests

import functions as bf
import database
import config
from modules import ddoser
from funclist import Funclist


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Anekdot:
    keywords = ['анекдот', 'анек', "шутка", "пошути", "юмореска"]
    commands = keywords
    attachment = []
    help_name = 'Анекдот'
    help_content = 'Бот пришлет вам случайный анекдот с анекдот.ру'
    help_deep = 'Использование:"бот анекдот", "бот анек"'

    def answer(self, message, vk, *rest):
        re = requests.get('https://www.anekdot.ru/rss/randomu.html')
        re.encoding = 'utf-8'
        text = re.text
        texts = text.split("JSON.parse('")[1]
        aneks = texts.split("');\nvar anekdot_i")[0]
        aneks = aneks.replace('\\\\\\"', "'").replace("\\\"", '"')
        aneks = json.loads(aneks)
        keyboard = dict(buttons=[[
            dict(action=dict(type="text", label="Ещё один анекдот"), color="primary"),
        ]], inline=True)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=choice(aneks), keyboard=keyboard)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Sing:
    keywords = ['спой']
    commands = keywords
    attachment = []
    help_name = 'Спой'
    help_content = 'бот пришлет дудос голосовыми'
    help_deep = 'Использование: "бот спой" '

    def answer(self, message, vk, *rest):
        answer = ''
        ddos = database.DDosDataBase.get()
        if ddos:
            config.logger.debug(ddos)
            new_ddoser = ddoser.Ddoser(vk, message.peer_id, ddos, 1, threading.currentThread().getName() + '_ddos')
            new_ddoser.start()
        else:
            answer = 'Не могу найти ни одного дудоса'
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


def upload_photo_to_vk_message(api, files, peer_id):
    url = api.photos.getMessagesUploadServer(type='photo', peer_id=peer_id).get('upload_url')
    url_2 = requests.post(url, files=files).text
    photo = json.loads(url_2)['photo']
    server = json.loads(url_2)['server']
    hash_ = json.loads(url_2)['hash']
    response_2 = api.photos.saveMessagesPhoto(photo=photo, server=server, hash=hash_)[0]
    id_ = response_2.get('id')
    owner_id = response_2.get('owner_id')
    attach = f'photo{owner_id}_{id_}'
    return attach


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Draw:
    keywords = ['нарисуй']
    commands = keywords
    attachment = []
    help_name = 'Нарисуй'
    help_content = 'бот нарисует симпатичного робота'
    help_deep = 'Бот рисует то, что вы попросили нарисовать. ' \
                'Если хотите получать разные картинки - просите нарисовать разные вещи\n' \
                'Использование: "бот нарисуй робота" или "бот нарисуй бабайку"'
    lock = threading.Lock()

    def answer(self, message, vk, *rest):
        h = md5((message.text + str(message.from_id)).encode()).hexdigest()
        r = requests.get(f'https://www.gravatar.com/avatar/{h}?d=robohash&s=512')
        files = {'photo': r.content}

        attach = upload_photo_to_vk_message(vk, files, message.peer_id)
        answer = 'Держи, я старался'

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, attachment=attach, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class SeeMe:
    keywords = ['изобрази', 'видишь', 'как', 'ты']
    commands = ['изобрази', 'как ты видишь']
    attachment = []
    help_name = 'Изобрази'
    help_content = 'бот скидывает фотографию, как он себе представляет'
    help_deep = 'Фотографии берутся с сайта thispersondoesnotexist.com \n' \
                'Использование: "бот изобрази админа" или "бот как ты видишь меня" '
    lock = threading.Lock()

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text, self.commands).strip()\
            .replace('?', '').replace('меня', 'тебя').replace('мою', 'твою')
        r = requests.get('https://thispersondoesnotexist.com/image')
        files = {'photo': r.content}
        attach = upload_photo_to_vk_message(vk, files, message.peer_id)
        answer = 'Я вижу ' + msg + ' так'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, attachment=attach, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class CatGenerator:
    keywords = ['котик', 'кот']
    commands = keywords
    attachment = []
    help_name = 'Котик'
    help_content = 'бот скидывает фотографию вымышленного кота'
    help_deep = 'Картинки берутся с thiscatdoesnotexist.com/ \n' \
                'Использование: "бот кот" или "бот котик" '
    lock = threading.Lock()

    def answer(self, message, vk, *rest):
        r = requests.get('https://thiscatdoesnotexist.com/')
        files = {'photo': r.content}
        attach = upload_photo_to_vk_message(vk, files, message.peer_id)
        answer = 'Держи кота'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, attachment=attach, mesfromuser=message)
