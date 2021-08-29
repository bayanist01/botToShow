# -*- coding: utf-8 -*-

import threading
import re
from vk_api.bot_longpoll import VkBotEventType

import functions
import config
import callbackHandler


def message2me(message):
    """Бот решает сообщение адресовано ему или нет"""
    match = re.search(rf'^([,<]jn|бот|/)|\[club{config.my_id}\|', message.text, re.I)
    return (
        message.peer_id < config.vk_groupchats_id_limit or
        match or
        message.get('reply_message', {}).get('from_id') == -int(config.my_id)
    )


class Worker(threading.Thread):

    def __init__(self, name, queue, workdone, vk, Funclist):
        """Инициализация потока"""
        super(Worker, self).__init__()
        self.name = name
        self.queue = queue
        self.workdone = workdone
        self.vk = vk
        self.Funclist = Funclist

    def run(self):
        """Запуск потока"""
        # бесконечный цикл
        while True:
            # берем из очереди, тут если что он умрет
            event = self.queue.get()

            try:
                # обработка кнопок
                if event.type == 'message_event':
                    callbackHandler.find_handler(self.vk, event)

                # обработка входящих сообщений
                elif event.type == VkBotEventType.MESSAGE_NEW:
                    if message2me(event.message):
                        functions.answer(event.message, True, self.vk, self.workdone, self.Funclist)

                else:
                    config.logger.debug(f'Новое событие: {event.type}')

            except Exception as e:
                config.logger.exception(e)
                if config.debug:
                    raise
            finally:
                # Отправляем сигнал о том, что задача завершена
                self.queue.task_done()

            config.logger.info(f'поток №{self.name} завершил свою задачу')
