# -*- coding: utf-8 -*-
import json

import functions as bf
import database
import config
from modules import ddoser
from funclist import Funclist


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AddDdos:
    keywords = ['дудос', 'добавь']
    commands = ['добавь дудос']
    attachment = []
    help_name = 'Добавь дудос'
    help_content = 'добавляет все кроме первой строки в текст дудоса по строкам. ' \
                   'Прикрепленную аудио добавляет в аудио дудоса'
    help_deep = 'Прикрепит в дудос первую найденную в сообщении аудиозапись. Каждая твоя строка ' \
                '(кроме первой на которой "бот добавь дудос") будет отдельным сообщением дудоса.\n' \
                'Не больше 12 строк\n' \
                'Использование: "бот добавь дудос\n' \
                'первое сообщение дудоса\n' \
                'второе сообщение дудоса\n' \
                '. . .' \
                'последнее сообщение дудоса\n' \
                'Аудиозапись"'

    def answer(self, message, vk, *rest):
        attachment = ''
        answer = ''
        at = message.attachments

        if at:
            for x in at:
                if x.get('type') == 'audio':
                    id_ = x.get('audio').get('id')
                    owner_id = x.get('audio').get('owner_id')
                    attachment = f'audio{owner_id}_{id_}'

            if not attachment:
                answer = answer + '\nНе нашел музыки'
        else:
            answer = answer + '\nНе нашел вложений в сообщении'

        ddostext = message.text.split('\n')

        if len(ddostext) > 1:
            ddostext = ddostext[1:]
        else:
            answer = answer + '\nСлишком короткий дудос. Не меньше одной строки'

        if len(ddostext) > 12:
            answer = answer + '\nСлишком длинный дудос. Не больше 12 строк'

        if not answer:
            ddos = [attachment] + [message.text.split('\n', 1)[1]]
            database.DDosDataBase.add(ddos)
            answer = 'Дудос добавлен'

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class AllDdoses:
    keywords = ['все', 'дудосы']
    commands = ['все дудосы']
    attachment = []
    help_name = 'Все дудосы'
    help_content = 'бот шлет список всех дудосов'
    help_deep = 'Смотришь на порядковый номер дудоса и можешь с ним взаимодействовать по номеру'

    def answer(self, message, vk, *rest):
        answer = ''
        ddoses = database.DDosDataBase.getall()
        if not ddoses:
            answer = 'Не нашел дудосов'
        for x in ddoses:
            answer += str(x[0]) + ') '
            for z in x[1:]:
                answer += z + '\n'
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class UpdateDdos:
    keywords = ['дудос', 'обнови']
    commands = ['обнови дудос']
    attachment = []
    help_name = 'Обнови дудос {id}'
    help_content = 'бот заменит текст и/или аудио в зависимости от того что есть в команде'
    help_deep = 'Использование: "бот обнови дудос 3 *прикрепленная новая аудиозапись" ' \
                'или "бот обнови дудос 4 (ШИФТ+ЭНТЕР и там строки с текстом)'

    def answer(self, message, vk, *rest):
        answer = ''
        msg = message.text.lower()

        msg_words = msg.replace('\n', ' ').split(' ')
        ddos_id = [int(x) for x in msg_words if x.isdigit()][0]
        oldddos = None
        if ddos_id:
            oldddos = database.DDosDataBase.getcur(ddos_id)
        if oldddos:
            oldddos = oldddos[0]
        if oldddos:
            oldattachment = oldddos[1]

            at = message.attachments
            attachment = None
            if at:
                for x in at:
                    if x.get('type') == 'audio':
                        id_ = x.get('audio').get('id')
                        owner_id = x.get('audio').get('owner_id')
                        attachment = 'audio%s_%s' % (str(owner_id), str(id_))

            if not attachment:
                attachment = oldattachment
            else:
                database.DDosDataBase.updatecur(ddos_id, [attachment, oldddos[2]])

            ddostext = message.text.split('\n')

            if len(ddostext) > 1:
                ddostext = ddostext[1:]
            else:
                answer = answer + '\nСлишком короткий дудос. Не меньше одной строки. ' \
                                  'Но вложение я заменю если ты прикрепил'

            if len(ddostext) > 12:
                answer = answer + '\nСлишком длинный дудос. Не больше 12 строк. ' \
                                  'Но вложение я заменю если ты прикрепил'

            if not answer:
                ddos = [attachment] + [message.text.split('\n', 1)[1]]
                database.DDosDataBase.updatecur(ddos_id, ddos)
                answer = 'Дудос обновлен'

        else:
            answer = answer + '\n Я не понял какой дудос обновить. Добавь сюда его номер'

        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class DeleteDdos:
    keywords = ['дудос', 'удали']
    commands = ['удали дудос']
    attachment = []
    help_name = 'Удали дудос {id} '
    help_content = 'бот удаляет дудос с заданным номером'
    help_deep = 'Использование: "бот удали дудос 14" '

    def answer(self, message, vk, *rest):
        answer = ''
        admins = [int(x) for x in json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))]
        if message.from_id in admins:
            msg = message.text.lower()
            msg_words = msg.replace('\n', ' ').split(' ')
            ddos_id = [int(x) for x in msg_words if x.isdigit()][0]
            if ddos_id:
                database.DDosDataBase.delete(ddos_id)
                answer = 'Удалил'
            else:
                answer = 'Я не понял какой дудос удалить. Добавь сюда его номер'
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.adminfunclist)
@bf.addtrigger(bf.standart_trigger)
class GetDdosById:
    keywords = ['дудос']
    commands = ['дудос']
    attachment = []
    help_name = 'Дудос {id}'
    help_content = 'бот шлет дудос по айди'
    help_deep = 'Для радости или проверки работоспособности дудосов. Можешь выбрать свой любимый\n' \
                'Использование: "бот дудос 2" '

    def answer(self, message, vk, *rest):
        answer = ''
        admins = [int(x) for x in json.loads(database.ForAllDataBase.getbyunique(config.my_id, 'admin_id'))]
        if message.from_id in admins:
            msg = bf.erase_command(message.text.lower(), self.commands)

            if msg:
                msg_words = msg.replace('\n', ' ').split(' ')
                ddos_id = [int(x) for x in msg_words if x.isdigit()][0]
            else:
                Ddos.answer(None, message, vk, *rest)
                return

            if ddos_id:
                ddos = database.DDosDataBase.getcur(ddos_id)

                if ddos:
                    ddos = ddos[0]
                if ddos:
                    ddos = ddos[1:]
                    config.logger.debug(ddos)
                    new_ddoser = ddoser.Ddoser(vk, message.peer_id, ddos)
                    new_ddoser.start()
                else:
                    answer = 'Не могу найти этого дудоса'

            else:
                answer = answer + '\n Я не понял какой дудос. Добавь сюда его номер'
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Ddos:
    keywords = ['дудос']
    commands = ['дудос']
    attachment = []
    help_name = 'Дудос'
    help_content = 'бот шлет песню и подпевает как может'
    help_deep = 'Дудос это когда бот кидает аудиозапись, а потом подпевает по строчке в сообщении.' \
                ' Но не переживайте, в нем не больше 13 сообщений\n' \
                'Использование: "бот дудос" '

    def answer(self, message, vk, *rest):
        answer = ''
        ddos = database.DDosDataBase.get()
        if ddos:
            config.logger.debug(ddos)
            new_ddoser = ddoser.Ddoser(vk, message.peer_id, ddos)
            new_ddoser.start()
        else:
            answer = 'Не могу найти ни одного дудоса'
        if answer:
            bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)
