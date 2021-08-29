# -*- coding: utf-8 -*-

from queue import Queue
import threading
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

# отсюда берем айдишник, токен, мой айдишник на всякий случай и тд
import config
import funclist
# тут логика ответов на вопросы
import modules
import functions
import database
import worker
import ReminderThread


def run_bot():
    # инициализация
    vk_session = vk_api.VkApi(token=config.token, api_version='5.124')
    longpoll = VkBotLongPoll(vk_session, config.my_id)
    vk = vk_session.get_api()
    database.init_databases()

    # ставим онлайн в сообществе
    try:
        a = vk.groups.getOnlineStatus(group_id=config.my_id)
        if a['status'] != 'online':
            vk.groups.enableOnline(group_id=config.my_id)
    except Exception as e:
        if 'Invalid request: too many starts per day' in str(e):
            pass
        else:
            config.logger.exception(e)

    queue = Queue()
    workdone = threading.Event()

    functions.sendmessage(vk, peer_id=config.creator_id, answer='Я родился!')

    workers = [worker.Worker(str(i + 1), queue, workdone, vk, funclist.Funclist) for i in range(config.workersneeded)]
    reminder_thread = ReminderThread.Reminder(vk, workdone)

    reminder_thread.start()
    for w in workers:
        w.setDaemon(True)
        w.start()

    config.logger.info('Запущен')

    # основной рабочий цикл
    while not workdone.is_set():
        config.logger.debug('Работаю')
        try:
            events = longpoll.check()
            for event in events:
                config.logger.debug(event)
                queue.put(event)
        except Exception as e:
            config.logger.exception(e)
            if config.debug:
                raise

    config.logger.warning('Выключаюсь')

    # ставим оффлайн в сообществе
    a = vk.groups.getOnlineStatus(group_id=config.my_id)
    if a['status'] == 'online':
        vk.groups.disableOnline(group_id=config.my_id)

    queue.join()
    reminder_thread.join()
    config.logger.warning('Я выключен')
    functions.sendmessage(vk, peer_id=config.creator_id, answer='Я уснул')


if __name__ == '__main__':
    run_bot()
