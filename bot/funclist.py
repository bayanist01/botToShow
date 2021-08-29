# -*- coding: utf-8 -*-

# класс со списками функций
class Funclist:
    # для нормальных команд по вызовам
    standartfunclist = []
    # админские команды
    adminfunclist = []
    # игры
    gamesfunclist = []
    # функционал для друзей
    friendfunclist = []
    # функционал для ридонли команд
    silentfunclist = []
    # на случай сообщения которое явно адресовано боту, но он не знает что ответить
    emptyfunclist = []

    # используется для поиска подробной информации о коммандах в команде команда :)
    searchlist = [standartfunclist, silentfunclist, adminfunclist, gamesfunclist, emptyfunclist, friendfunclist]

