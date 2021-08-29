# -*- coding: utf-8 -*-

import html
import json
import re
import requests

import functions as bf
from funclist import Funclist

more_keyboard = dict(buttons=[[dict(action=dict(type='text', label='Ещё один чгк вопрос'), color='primary'), ]],
                     inline=True)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class ChgkAnswer:
    keywords = ['ответ']
    commands = keywords
    attachment = []
    help_name = 'Ответ'
    help_content = 'Бот пришлет вам ответ на вопрос с db.chgk.info'
    help_deep = 'Использование: только по кнопке'

    def answer(self, message, vk, *rest):
        if not message.payload:
            return
        ans = json.loads(message.payload).get('ans')
        bf.sendmessage(vk, peer_id=message.peer_id, answer=ans, keyboard=more_keyboard)


def parse_question(text):
    q = re.findall(r'<strong>Вопрос 1:</strong>([^♥]*?)<p>', text)[0]
    q = html.unescape(q)
    q = re.findall(r'(?:>|^)([^<>]+)(?:<|$)', q)
    q = [x.strip() for x in q if x.strip()]
    q = ' '.join(q)
    q = q.replace('\n', ' ')
    return q


def parse_answer(text):
    a = re.findall(
        r'<p>(?:.|[\n])+?((?:<strong>Ответ:</strong>|<strong>Зачёт:</strong>|<strong>Комментарий:</strong>)'
        r'(?:.|[\n])+?)</p>',
        text)
    a = ' '.join(a)
    a = html.unescape(a)
    a = re.findall(r'(?:>|^)([^<>]+)(?:<|$)', a)
    a = [x.strip() for x in a if x.strip()]
    a = ' '.join(a)
    a = a.replace('\n', ' ').replace('Зачёт:', '\nЗачёт:').replace('Комментарий:', '\nКомментарий:')
    return a


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class ChgkQuestion:
    keywords = ['чгк']
    commands = keywords
    attachment = []
    help_name = 'ЧГК'
    help_content = 'Бот пришлет вам случайный вопрос с db.chgk.info'
    help_deep = 'Использование:"бот чгк"'

    def answer(self, message, vk, *rest):

        req = requests.get('https://db.chgk.info/random/answers/limit1')
        rt = req.text
        rt = re.findall(r"<div class='random_question'>([^♥]*?)</div>", rt)[0]

        q = parse_question(rt)
        a = parse_answer(rt)
        answers = []

        while len(a) > 200:
            split = a.find(' ', 200)
            answers.append(a[:split])
            a = a[split:]
        else:
            answers.append(a)

        # button [0][0] payload should be not more than 255 letters length

        keyboard = dict(buttons=[], inline=True)
        payload = dict(ans='', ensure_ascii=False)
        buttonrow = [
            dict(action=dict(type='text', label='Показать ответ', payload=''),
                 color='primary'),
        ]

        for i, x in enumerate(answers, 1):
            buttonrow[0]['action']['label'] = f'Показать ответ. Часть №{i}'
            payload['ans'] = x
            buttonrow[0]['action']['payload'] = json.dumps(payload)

            keyboard['buttons'].append(buttonrow.copy())

        bf.sendmessage(vk, peer_id=message.peer_id, answer=q, keyboard=keyboard)
