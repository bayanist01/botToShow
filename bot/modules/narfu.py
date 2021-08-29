# -*- coding: utf-8 -*-
import html
import re
import requests
from datetime import datetime, timedelta

import functions as bf
import database as database
import config as config
from funclist import Funclist


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class SetGroup:
    keywords = ['группа']
    commands = keywords
    attachment = []
    help_name = 'Группа'
    help_content = 'Бот запомнит вашу группу (по сайту с расписанием)'
    help_deep = 'Использование: "бот группа 9999", цифры брать из ссылки с расписания'

    def answer(self, message, vk, *rest):
        group = re.findall(r'[0-9]+', message.text)[0]

        if database.ForAllDataBase.getbyunique(int(message.peer_id), 'narfu_group'):
            database.ForAllDataBase.update(int(message.peer_id), 'narfu_group', group)
        else:
            database.ForAllDataBase.add(int(message.peer_id), 'narfu_group', group)

        bf.sendmessage(vk, peer_id=message.peer_id, answer="Сохранил, ещё раз проверьте что вы скинули мне номер"
                                                           " группы из https://ruz.narfu.ru/?timetable&group=ТУТНОМЕР,"
                                                           " а не номер группы шестизначный")


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Raspisanie:
    keywords = ['расписание', 'пары', 'test']
    commands = keywords
    attachment = []
    help_name = 'Расписание'
    help_content = 'Бот пришлет вам расписание сафу'
    help_deep = 'Использование: "бот расписание" или "бот пары" или "бот пары завтра" или "бот расписание на завтра"'

    def answer(self, message, vk, *rest):
        ans = ''
        error = ''
        group = database.ForAllDataBase.getbyunique(int(message.peer_id), 'narfu_group')

        if not group:
            ans = 'Я не знаю вашей группы. "бот группа 9999" - команда чтобы сообщить мне его. Номер брать с сайта' \
                  ' расписания: https://ruz.narfu.ru/?timetable&group=ТУТНОМЕР'

        if not ans:
            try:
                req = requests.get(f'https://ruz.narfu.ru/?timetable&group={int(group)}')
                req.encoding = 'utf-8'

                day = (datetime.today() + timedelta(days=(1 if 'завтра' in message.text.lower() else 0),
                                                    hours=(0 if 'сегодня' in message.text.lower() else 8))).strftime(
                    '%d.%m.%Y')

                days = re.findall(r'<div class="list(?: last)? col-md-2([^♥]*?)<!-- list -->', req.text)
                classes = [x for x in days if re.findall(r'[0-9]{2}.[0-9]{2}.[0-9]{4}', x)[0] == day][0]
                classes = re.findall(r'<div class="timetable_sheet_xs visible-xs visible-sm([^♥]*?)</div>', classes)
                result = []

                for clas in classes:
                    result.append(dict(num_para=re.findall(r'<span class="num_para">([^♥]*?)</span>', clas)[0],
                                       time_para=html.unescape(
                                           re.findall(r'<span class="time_para">([^♥]*?)</span>', clas)[0].strip()),
                                       kind_of_work=re.findall(r'<span class="kindOfWork">([^♥]*?)</span>', clas)[0],
                                       discipline=re.findall(r'<span class="discipline">([^♥]*?)</span>', clas)[0],
                                       lecturer=re.findall(r'<span class="lecturer">([^♥]*?)</span>', clas),
                                       auditorium=html.unescape(re.findall(r'<b>([^♥]*?)</b>', clas)[0].strip()),
                                       group=re.findall(r'<span class="group">([^♥]*?)</span>', clas)
                                       ))

                # 📗📘📙📕
                emoji = {'Практические занятия': '📙', 'Лабораторные занятия': '📘', 'Лекции': '📗', 'empty': '📕'}
                for x in result:
                    ans += f'{x.get("num_para")}) ' \
                           f'{emoji.get(x.get("kind_of_work")) if x.get("kind_of_work") in emoji else emoji["empty"]}' \
                           f'{x.get("discipline")}\n' \
                           f'{x.get("time_para")} {x.get("kind_of_work")} ' \
                           f'{x.get("lecturer")[0] if x.get("lecturer") else ""}\n' \
                           f'{x.get("auditorium")} {x.get("group")[0] if x.get("group") else ""}\n'

                if not ans:
                    ans = 'Я не нашел пар или их в указанный день нет'

                ans = f'{day}:\n{ans}'

            except Exception as e:
                bf.sendmessage(vk, peer_id=config.creator_id, answer=f'Ошибка в запросе расписания: {e}')

        bf.sendmessage(vk, peer_id=message.peer_id, answer=ans)
