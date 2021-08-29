# -*- coding: utf-8 -*-

import threading
from time import sleep

import functions
import config
import modules.smalltalks as smalltalks


class Message:
    def __init__(self, text, peer):
        self.text = text
        self.peer_id = peer


class Ddoser(threading.Thread):

    def __init__(self, vk, peer, ddos, sing=0, name='ddos'):
        """Инициализация потока"""
        super(Ddoser, self).__init__()
        self.vk = vk
        self.ddos = ddos
        self.peer = peer
        self.sing = sing
        self.name = name

    def run(self):
        try:
            attach = self.ddos[0]
            functions.sendmessage(self.vk, peer_id=self.peer, attachment=attach)
            if not self.sing:
                sleep(1)
                for x in self.ddos[1].split('\n'):
                    functions.sendmessage(self.vk, peer_id=self.peer, answer=x)
                    sleep(3)
            else:
                smalltalks.Say.answer(Message(self.ddos[1], self.peer), self.vk)
        except Exception as e:
            config.logger.exception(e)
