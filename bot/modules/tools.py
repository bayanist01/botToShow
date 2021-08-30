# -*- coding: utf-8 -*-
import json
import requests
import wikipedia
from googletrans import Translator
from datetime import timezone, timedelta, datetime

import config
import database
import functions as bf
from funclist import Funclist
from texts import texts


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.attachment_trigger)
class QRscanner:
    commands = []
    keywords = []
    attachment = ['photo']
    help_name = 'QR-код'
    help_content = 'в ответ на фотографию бот скинет вам то что зашифровано в QR-коде'
    help_deep = 'Если не получится - сфоткайте получше, используется сторонний сервис, я над ним не властен.'

    def answer(self, message, vk, *rest):
        photo = (message.attachments[0])['photo']['sizes'][-1]['url']

        qrscannerurl = 'https://zxing.org/w/decode'
        req = requests.get(qrscannerurl, params={'u': photo})

        if 'Decode Succeeded' in req.text:
            text = req.text.split('<pre>', 1)[1].split('</pre>', 1)[0].replace('amp;', '')
        else:
            text = 'Хорошая фотография, но qr-кода я на ней не вижу, если вы об этом'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=text)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Wiki:
    keywords = ['что', 'такое', 'кто', 'такой']
    commands = ['что такое', 'кто такой']
    attachment = []
    help_name = 'Что такое/Кто такой'
    help_content = 'бот ищет в википедии'
    help_deep = 'Использование: "бот кто такой Галушин" или "бот что такое осень" '

    def answer(self, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), self.commands).strip()
        if not msg:
            ans = 'Я не понял что надо найти'
        else:
            wikipedia.set_lang("ru")

            wikiresults = wikipedia.search(msg.title(), results=3)
            ans = ''
            # Максимальная длина сообщения — 4096 знаков с пробелами
            for i, x in enumerate(wikiresults, 1):
                try:
                    res = wikipedia.summary(x)
                    if len(res) > 900:
                        res = wikipedia.summary(x, chars=900)

                    ans += f'{i}){res}...\n{wikipedia.page(x).url}\n'

                except wikipedia.exceptions.DisambiguationError:
                    pass
            if not ans:
                ans = 'Я ничего не смог найти'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=ans, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class MyTranslator:
    keywords = ['перевод']
    commands = keywords
    attachment = []
    help_name = 'Перевод'
    help_content = 'бот переводит фразу с любого на русский или с русского на английский'
    help_deep = 'Используется гугл переводчик. Все претензии по качеству перевода - к ним. \n' \
                'Использование: "бот перевод Привет" или "бот перевод hi" '

    @classmethod
    def answer(cls, message, vk, *rest):
        msg = bf.erase_command(message.text.lower(), cls.commands).strip()
        t = Translator()
        detect = t.detect(msg)
        if detect.lang != 'ru':
            answer = t.translate(msg, dest='ru').text
        else:
            answer = t.translate(msg).text
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Weather:
    keywords = ['погода']
    commands = keywords
    attachment = []
    help_name = 'Погода'
    help_content = 'выдает погоду в указаном городе или в городе из вашего профиля если город не указан'
    help_deep = 'Использование: "бот погода" - погода сейчас в городе из вашего профиля\n' \
                '"бот погода Москва" - погода сейчас в Москве\n' \
                '"бот погода (город) сегодня" - погода на сегодня подробнее чем просто сейчас\n' \
                '"бот погода (город) завтра" - погода на завтра\n' \
                'Скобки писать не надо. Пишите как в первых двух примерах. Либо город либо ничего'

    def answer(self, message, vk, *rest):
        msg = message.text.lower().strip()
        msg = bf.erase_command(msg, self.commands)
        msg = msg.strip()
        ans = None
        if 'сегодня' in msg or 'завтра' in msg:
            msg2 = bf.erase_command(msg, ['сегодня', 'завтра'])
            msg2 = msg2.strip()
            if msg2:
                # weather in msg city
                city = msg2.replace(' ', '+')
            else:
                # weather in profile city
                city = vk.users.get(user_ids=message.from_id, fields='city')[0].get('city').get('title')
                city = city.replace(' ', '+')

            r = requests.get('http://wttr.in/' + city + '?format=j1&lang=ru&m')
            r = json.loads(r.text)
            config.logger.debug(r)
            current_condition = r['current_condition'][0]
            ans = 'Сейчас в ' + city.replace('+', ' ').capitalize() + ':\n'
            C = current_condition['lang_ru'][0]['value']
            t = current_condition['temp_C']
            f = current_condition['FeelsLikeC']
            w = f"{current_condition['windspeedKmph']} {current_condition['winddir16Point']}"
            w = w.replace('N', 'С').replace('S', 'Ю').replace('W', 'З').replace('E', 'В')
            p = current_condition['precipMM']
            h = current_condition['humidity']

            ans += f'{C}\nТемпература:{t}, Ощущается как:{f}\nВетер:{w}\nОсадки:{p}\nВлажность:{h}\n'

            for i in ([r['weather']['завтра' in msg]]):
                ans += f'======{i["date"]}\n'
                for x in i['hourly']:
                    ans += '=== В ' + str(int(int(x['time']) / 100)) + ' часов будет:\n'
                    C = x['lang_ru'][0]['value']
                    t = x['tempC']
                    f = x['FeelsLikeC']
                    w = x['windspeedKmph'] + ' ' + x[
                        'winddir16Point'].replace('N', 'С').replace('S', 'Ю').replace('W', 'З').replace('E', 'В')
                    p = x['precipMM']
                    h = x['humidity']
                    ans += f'{C}\nТемпература:{t}, Ощущается как:{f}\nВетер:{w}\nОсадки:{p}\nВлажность:{h}\n'
        else:
            if msg:
                # weather in msg city
                city = msg.replace(' ', '+')
            else:
                # weather in profile city
                city = vk.users.get(user_ids=message.from_id, fields='city')[0].get('city').get('title')
                city = city.replace(' ', '+')
            r = requests.get(
                f'http://wttr.in/{city}?format=%C+%c\n'
                f'Температура:%t,+Ощущается+как:%f\n'
                f'Ветер:%w\n'
                f'Осадки:%p\n'
                f'Влажность:%h&lang=ru&m'
            )
            ans = 'Сейчас в ' + city.replace('+', ' ').capitalize() + ':\n' + r.text

        if ans:
            bf.sendmessage(vk, answer=ans, peer_id=message.peer_id, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Reminder:
    keywords = ['напомни']
    commands = ['напомни']
    attachment = []
    help_name = 'Напомни'
    help_content = 'бот напомнит вам в указанное время и дату'
    help_deep = 'Не вводите дату несуществующую, или меньшую, чем сегодняшняя ' \
                'Цифры надо писать цифрами, ненужные можно упускать, например: ' \
                'бот напомни через 2 часа 3 минуты 5 секунд 4 дня 3 месяца 7 лет (здесь то о чем надо напомнить)' \
                'бот напомни через 3 дня (здесь то о чем надо напомнить)' \
                'бот напомни в 12:10 14.09.21 (здесь то о чем надо напомнить)' \
                'бот напомни в 12:10 14.09.2021 (здесь то о чем надо напомнить)' \
                'бот напомни в 13:45 (здесь то о чем надо напомнить)' \
                'бот напомни 14.09 (здесь то о чем надо напомнить)' \
                'Время указывается московское '

    @staticmethod
    def str2date(msg_str):
        s = msg_str.split(' ')
        dt = {'hour': 0, 'minute': 0, 'second': 0, 'day': 0, 'month': 0, 'year': 0}
        for i in range(len(s)):
            if 'час' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['hour'] = abs(int(s[i - 1]))
                else:
                    dt['hour'] = 1
            elif 'минут' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['minute'] = abs(int(s[i - 1]))
                else:
                    dt['minute'] = 1
            elif 'сек' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['second'] = abs(int(s[i - 1]))
                else:
                    dt['second'] = 1
            elif 'дн' in s[i] or 'день' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['day'] = abs(int(s[i - 1]))
                else:
                    dt['day'] = 1
            elif 'месяц' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['month'] = abs(int(s[i - 1]))
                else:
                    dt['month'] = 1
            elif 'недел' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['day'] = abs(int(s[i - 1]) * 7)
                else:
                    dt['day'] = 7
            elif 'год' in s[i] or 'лет' in s[i]:
                if i != 0 and s[i - 1].isdigit():
                    dt['year'] = abs(int(s[i - 1]))
                else:
                    dt['year'] = 1
        return dt

    @staticmethod
    def cutdate(dt):
        while dt['second'] > 59:
            dt['second'] = dt['second'] - 60
            dt['minute'] = dt['minute'] + 1
        while dt['minute'] > 59:
            dt['minute'] = dt['minute'] - 60
            dt['hour'] = dt['hour'] + 1
        while dt['hour'] > 23:
            dt['hour'] = dt['hour'] - 24
            dt['day'] = dt['day'] + 1

        while dt['month'] > 11:
            dt['month'] = dt['month'] - 12
            dt['year'] = dt['year'] + 1
        return dt

    @staticmethod
    def cutstrtodigits(s: str):
        for i in s:
            if i.isalpha():
                s = s.replace(i, '')
        return s

    def answer(self, message, vk, *rest):
        msg = message.text.lower()
        tz = timezone(timedelta(hours=3))
        ansdt = None

        if message.peer_id < config.vk_groupchats_id_limit:
            tome = True
        elif 'мне' in msg:
            tome = True
        else:
            tome = False

        if 'через' in msg:
            dt = self.str2date(msg)
            time = message.date
            dt = self.cutdate(dt)
            time += dt['second'] + 60 * (dt['minute'] + 60 * (dt['hour'] + 24 * dt['day']))
            data = datetime.fromtimestamp(time, tz=tz)
            deltayear = (data.month + dt['month']) // 12
            dt['month'] = (data.month + dt['month']) % 12
            ansdt = datetime(data.year + deltayear + dt['year'], dt['month'], data.day,
                             data.hour, data.minute, data.second, tzinfo=tz)
            ansdt = datetime.timestamp(ansdt)
        else:
            msg = self.cutstrtodigits(msg)
            msg = msg.strip()
            now = datetime.now(tz)
            dt = {'hour': now.hour, 'minute': now.minute, 'second': now.second,
                  'day': now.day, 'month': now.month, 'year': now.year}
            time = [x for i in msg.split(' ') if i.find(':') > 0 for x in i.split(':')]
            time = [int(x) for x in time]
            if time:
                if len(time) > 0:
                    dt['hour'] = time[0]
                if len(time) > 1:
                    dt['minute'] = time[1]
                if len(time) > 2:
                    dt['second'] = time[2]
            date = [x for i in msg.split(' ') if i.find('.') > 0 for x in i.split('.')]
            date = [int(x) for x in date]
            if date:
                if len(date) > 0 and date[0]:
                    dt['day'] = date[0]
                if len(date) > 1 and date[1]:
                    dt['month'] = date[1]
                if len(date) > 2 and date[2]:
                    dt['year'] = date[2] if date[2] > 100 else date[2] + 2000
            dt = self.cutdate(dt)
            if not time and not date:
                ansdt = None
            else:
                try:
                    ansdt = datetime(dt['year'], dt['month'], dt['day'],
                                     dt['hour'], dt['minute'], dt['second'], tzinfo=tz)
                    ansdt = datetime.timestamp(ansdt)
                except Exception as e:
                    if 'day is out of range for month' in str(e):
                        ansdt = None
                    elif '[Errno 22] Invalid argument' in str(e):
                        ansdt = None
                    else:
                        raise
                if ansdt < datetime.timestamp(now):
                    ansdt += 60 * 60 * 24
                    if ansdt < datetime.timestamp(now):
                        ansdt = None

        if ansdt:
            toadd = [ansdt, message.from_id, message.peer_id, message.id, message.text, int(tome)]
            database.ReminderDataBase.addremind(toadd)
            answer = f"Напоминание установлено на {datetime.fromtimestamp(ansdt, tz=tz).strftime('%H:%M:%S %d.%m.%y')} " \
                     f"напомню {'тебе в личку' if tome else 'сюда'}"
        else:
            answer = None

        if not answer:
            answer = '''Я не понял когда напомнить, напоминание не установлено
            Возможно ты ввел дату несуществующую, или меньшую, чем сегодняшняя
            Цифры надо писать цифрами, ненужные можно упускать, например:
                бот напомни через 2 часа 3 минуты 5 секунд 4 дня 3 месяца 7 лет (здесь то о чем надо напомнить)
                бот напомни через 3 дня (здесь то о чем надо напомнить)
                бот напомни в 12:10 14.09.21 (здесь то о чем надо напомнить)
                бот напомни в 12:10 14.09.2021 (здесь то о чем надо напомнить)
                бот напомни в 13:45 (здесь то о чем надо напомнить)
                бот напомни 14.09 (здесь то о чем надо напомнить)
            Время указывается московское'''
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class PuntoSwitcher:
    commands = ["раскладка", 'hfcrkflrf']
    keywords = ["раскладка", 'hfcrkflrf']
    attachment = []
    help_name = 'Раскладка'
    help_content = 'бот меняет раскладку сообщения'
    help_deep = 'Использование: "бот раскладка ghbdtn" или "/hfcrkflrf ghbdtn" в зависимости от раскладки.' \
                ' Если написал просто "бот раскладка" то он будет искать что перевести в пересланных сообщениях'

    def answer(self, message, vk, *rest):
        answer = bf.erase_command(message.text, self.commands)

        if answer.isspace() or answer == '':
            if message.fwd_messages:
                answer = ''
                for i in message.get('fwd_messages'):
                    answer += '\n'
                    answer += i['text']
            if message.reply_message:
                answer = message.get('reply_message')['text']
        ans = ''
        rus = True
        for i in answer:
            if i in "abcdefghijklmnopqrstuvwxyz":
                rus = False
                break
            if i in "йцукенгшщзхъфывапролджэячсмитьбю":
                rus = True
                break
        if not rus:
            for i in answer:
                if i in texts.translit_en_ru:
                    ans += texts.translit_en_ru[i]
                else:
                    ans += i
        else:
            for i in answer:
                if i in texts.translit_ru_en:
                    ans += texts.translit_ru_en[i]
                else:
                    ans += i
        if ans == '' or ans.isspace():
            ans = 'Я не нашел что изменить'

        bf.sendmessage(vk, peer_id=message.peer_id, answer=ans, mesfromuser=message)
