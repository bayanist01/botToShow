# -*- coding: utf-8 -*-
import json
from random import choice

import functions as bf
import database
import texts.texts as texts
from funclist import Funclist

rps_keyboard = keyboard = dict(buttons=[[
            dict(action=dict(type='callback', label='Камень', payload='0'), color='primary'),
            dict(action=dict(type='callback', label='Ножницы', payload='1'), color='primary'),
            dict(action=dict(type='callback', label='Бумага', payload='2'), color='primary')
        ]], inline=True)


@bf.register(Funclist.gamesfunclist)
@bf.addtrigger(bf.standart_trigger)
class TwisterGame:
    keywords = ['твистер']
    commands = keywords
    attachment = []
    help_name = 'Твистер'
    help_content = 'бот скажет какую конечность на какой цвет поставить'
    help_deep = 'Если у вас самодельный твистер или набор цветов не совпадает с предложенным можете написать ' \
                '"бот твистер красный,розовый,оранжевый,голубенький" (обязательно через запятую) ' \
                'и он будет выбирать из предложенных вами цветов.' \
                ' Это сохранится в беседке пока вы не поменяете цвета таким же образом\n' \
                'Использование: "бот твистер" или "бот твистер цвет1,цвет2,цвет3,цвет4" '

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        db = database.ForAllDataBase.getbyunique(message.peer_id, 'twistergame')
        update = True if db else False
        if msg:
            colors = msg.split(',')
        else:
            if update:
                colors = json.loads(db)
            else:
                colors = ['Красный', 'Синий', 'Желтый', 'Зеленый']
        if update:
            database.ForAllDataBase.update(message.peer_id, 'twistergame', json.dumps(colors))
        else:
            database.ForAllDataBase.add(message.peer_id, 'twistergame', json.dumps(colors))
        answer = f'{choice(["Правую", "Левую"])} {choice(["ногу", "руку"])} на {choice(colors)}'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.gamesfunclist)
@bf.addtrigger(bf.standart_trigger)
class Inever:
    keywords = ['я', 'никогда', 'не']
    commands = ['я никогда не']
    attachment = []
    help_name = 'Я никогда не'
    help_content = 'бот выдает фразу из "я никогда не". Что делать с теми кто делал - решайте сами'
    help_deep = 'Старая добрая "Я никогда не" теперь прямо в беседе. \n' \
                'Использование: "бот я никогда не" - он выдаст'

    def answer(self, message, vk, *rest):
        answer = choice(texts.i_never)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.gamesfunclist)
@bf.addtrigger(bf.standart_trigger)
class Truedotrue:
    keywords = ['правда']
    commands = ['правда']
    attachment = []
    help_name = 'Правда'
    help_content = 'бот выдает вопрос из "Правды или действия"'
    help_deep = 'Использование: "бот правда" '

    def answer(self, message, vk, *rest):
        answer = choice(texts.true)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.gamesfunclist)
@bf.addtrigger(bf.standart_trigger)
class Truedodo:
    keywords = ['действие']
    commands = ['действие']
    attachment = []
    help_name = 'Действие'
    help_content = 'бот выдает задание из "Правды или действия"'
    help_deep = 'Использование: "бот действие" '

    def answer(self, message, vk, *rest):
        answer = choice(texts.do)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.gamesfunclist)
@bf.addtrigger(bf.standart_trigger)
class RockPaperScissors:
    keywords = ['камень', 'ножницы', 'бумага', 'цу', 'е', 'фа', 'цуефа']
    commands = ['цуефа', 'камень ножницы бумага']
    attachment = []
    help_name = 'Цуефа'
    help_content = 'вызывает собеседников на поединок в камень-ножницы-бумага'
    help_deep = 'Работает только с телефона потому что при нажатии на кнопку с компа ' \
                'он отправляет сообщение с текстом кнопки, что рушит анонимность. ' \
                'В личке играешь с ботом, в беседе - кто первые нажали на кнопку те и играют. ' \
                'Индикатор загрузки на кнопке это глюки ВК. Бот твой ответ получил, не переживай\n' \
                'Использование: "бот цуефа" или "бот камень ножницы бумага" а потом жмешь на кнопку в сообщении и ждешь соперника'

    def answer(self, message, vk, *rest):
        answer = 'Выбирай свой ответ \n Работает только с телефона'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, keyboard=rps_keyboard, mesfromuser=message)
