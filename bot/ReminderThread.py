# -*- coding: utf-8 -*-

import json
import random
import threading
from time import sleep
from datetime import datetime
import requests
import vk_api

import functions
import database
import config
from texts import texts


class Reminder(threading.Thread):

    def __init__(self, vk, workdone):
        """Инициализация потока"""
        super(Reminder, self).__init__()
        self.workdone = workdone
        self.vk = vk
        self.today = None

    def run(self):
        """Запуск потока"""
        config.logger.info('Напоминатель приступает')
        # бесконечный цикл
        while not self.workdone.is_set():
            # тут работать
            datenow = datetime.now()
            now = int(datenow.timestamp())

            if self.today != datenow.date():
                self.today = datenow.date()
                str_today = self.today.strftime('%d.%m.%%')
                users = database.ForAllDataBase.getbydate('bdate', str_today)

                for x in users:
                    happy_birthday(self.vk, x[0])

            if ((now + 4*60*60) % 43200) < config.reminder_sleeps:      # 43200 sec = 12 hour
                wall_post_neuro_cat()
                config.logger.info('Neurocat was posted')

            reminderfromdb = database.ReminderDataBase.getremind(now)

            for rem in reminderfromdb:
                functions.sendmessage(self.vk, peer_id=(rem.user_id if rem.to_me else rem.peer_id),
                                      answer=f'[id{str(rem.user_id)}|'
                                             f'{self.vk.users.get(user_ids=rem.user_id)[0].get("first_name")}],' 
                                             f' напоминаю: \n'
                                             f'{(f"<<{rem.message_text}>>" if not rem.message_id else "")}',
                                      fwd_messages=rem.message_id)

            # это чтобы не ждать 30 сек для перезапуска пока он проверит флаг завершения работы
            sleep(config.reminder_sleeps if not config.debug else 3)

        config.logger.warning('поток Напоминатель завершил работу')


def happy_birthday(vk, uid):
    if vk.messages.isMessagesFromGroupAllowed(group_id=config.my_id, user_id=uid)['is_allowed']:
        functions.sendmessage(vk, peer_id=uid, answer=random.choice(texts.bdate))


def getcat():
    r = requests.get('https://thiscatdoesnotexist.com/')
    return r.content


def upload_cat_to_vk(api, group_id, cat_bytes):
    files = {'photo': ('catofday.jpg', cat_bytes)}
    url = api.photos.getWallUploadServer(group_id=group_id).get('upload_url')
    url_2 = requests.post(url, files=files).text

    photo = json.loads(url_2)['photo']
    server = json.loads(url_2)['server']
    hash_ = json.loads(url_2)['hash']

    response_2 = api.photos.saveWallPhoto(group_id=group_id, photo=photo, server=server, hash=hash_)[0]
    id_ = response_2.get('id')  # получаю id файла
    owner_id = response_2.get('owner_id')

    attach = f'photo{owner_id}_{id_}'

    return attach, url_2


def wall_post_neuro_cat():
    vk_session2 = vk_api.VkApi(token=config.user_token)
    vk2 = vk_session2.get_api()
    groupid = int(config.my_id)

    cat_bytes = getcat()
    attach, url = upload_cat_to_vk(vk2, groupid, cat_bytes)

    vk2.wall.post(
        owner_id=-groupid,
        message='Нейрокот для твоей ленты!\nХочешь больше таких? Пиши в сообщения "кот"\n#нейрокот',
        from_group=1,
        signed=0,
        guid=str(url),
        attachments=attach,
        copyright='https://thiscatdoesnotexist.com/'
    )

