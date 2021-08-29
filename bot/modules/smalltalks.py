# -*- coding: utf-8 -*-
import json
import threading
from datetime import datetime
from random import choice, randint
import requests
from gtts import gTTS

import functions as bf
import config
from funclist import Funclist
from texts import texts, changeandversion


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class WhatsNew:
    keywords = ['что', 'нового']
    commands = ['что нового']
    attachment = []
    help_name = 'Что нового'
    help_content = 'Скажет что изменилось с последней версии'
    help_deep = 'Использование: "бот что нового" '

    def answer(self, message, vk, *rest):
        answer = changeandversion.version_changelog[0][1]
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class ThankYou:
    keywords = ['спасибо', 'спс']
    commands = keywords
    attachment = []
    help_name = 'Спасибо'
    help_content = 'Можете поблагодарить бота за что-то полезное'
    help_deep = 'Использование:"бот спасибо", "бот спс"'

    def answer(self, message, vk, *rest):
        anses = ['Не за что!', 'Вам спасибо!', 'Рад был полезным!', 'Спасибо на хлеб не положишь с:', 'Рад стараться!']
        bf.sendmessage(vk, peer_id=message.peer_id, answer=choice(anses))


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class WhatAreYouDoing:
    keywords = ['что', 'делаешь']
    commands = ['что делаешь']
    attachment = []
    help_name = 'Что делаешь'
    help_content = 'бот отвечает на этот вопрос'
    help_deep = 'Фразы берутся с сайта godville.net \n' \
                'Использование: "бот что делаешь" или "бот что делаешь?"'

    def answer(self, message, vk, *rest):
        r = json.loads(requests.get(config.godville_url).text)
        answer = 'Пытаюсь ' + r['quest']
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Agree:
    keywords = ['что', 'скажи', 'подтверди']
    commands = ['скажи что', 'подтверди']
    attachment = []
    help_name = 'Подтверди'
    help_content = 'соглашается с вами'
    help_deep = 'Использование: "бот скажи что коты крутые" или "бот подтверди что я прав" '

    def answer(self, message, vk, *rest):
        answer = choice(texts.agree)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Repeat:
    keywords = ['повтори']
    commands = keywords
    attachment = []
    help_name = 'Повтори'
    help_content = 'повторит вашу фразу'
    help_deep = 'Использование: "бот повтори ололо" (бот ответит "ололо")'

    def answer(self, message, vk, *rest):
        msg = message.text
        msg = bf.erase_command(msg, self.commands).strip()
        if msg:
            answer = bf.anti_troll(msg)
        else:
            answer = 'Я не нашел что повторить'
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class WhatsUp:
    keywords = ['как', 'дела']
    commands = ['как дела']
    attachment = []
    help_name = 'Как дела'
    help_content = 'бот отвечает на этот вопрос'
    help_deep = 'Фразы берутся с godville.net\n' \
                'Использование: "бот как дела" или "бот как дела?" '

    def answer(self, message, vk, *rest):
        r = json.loads(requests.get(config.godville_url).text)
        answer = r['diary_last']
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Say:
    keywords = ['скажи']
    commands = ['скажи']
    attachment = []
    help_name = 'Скажи'
    help_content = 'бот отправляет голосовое с текстом'
    help_deep = 'Бот скинет ваш текст голосом Пасюка!\n' \
                'Использование: "бот скажи я занимаюсь руферством"'

    @classmethod
    def answer(cls, message, vk, *rest):
        answer = ''
        attach = ''
        msg = bf.erase_command(message.text, cls.commands)
        msg = bf.anti_troll(msg)
        msg = msg.strip()

        if len(msg) > 400:
            answer = 'Сообщение слишком длинное'
        else:
            if msg and not msg.isspace():
                tts = gTTS(msg, lang='ru')
                name = str(threading.currentThread().getName()) + '.mp3'
                config.logger.debug(name)
                tts.save(name)

                url = vk.docs.getMessagesUploadServer(type='audio_message', peer_id=message.peer_id).get('upload_url')
                files = [('file', (name, open(name, 'rb')))]
                url_2 = requests.post(url, files=files).text
                response = json.loads(url_2)['file']
                response_2 = vk.docs.save(file=response)
                id = response_2.get('audio_message').get('id')
                owner_id = response_2.get('audio_message').get('owner_id')

                attach = 'doc%s_%s' % (str(owner_id), str(id))

            else:
                answer = 'Не нашел что я должен сказать'

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, attachment=attach)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.just_in_trigger)
class Magic8:
    keywords = ['?']
    commands = ['?']
    attachment = []
    help_name = '?'
    help_content = 'бот отвечает на ваш вопрос как магический шар 8'
    help_deep = 'Задай вопрос с ответом Да или Нет. Бот ответит\n' \
                'Использование: "бот я единорог?" '

    def answer(self, message, vk, *rest):
        answer = choice(texts.magic8)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class When:
    keywords = ["когда"]
    commands = keywords
    attachment = []
    help_name = 'Когда'
    help_content = 'бот предскажет точную дату'
    help_deep = 'Использование: "бот когда что-то" - выдаст случайную дату\n' \
                '"бот когда нг" или "бот когда новый год" - подскажет сколько осталось ждать \n' \
                '"бот когда др" или ' \
                '"когда день рождения" - скажет точно сколько осталось до твоего дня рождения с точностью до секунд'

    def answer(self, message, vk, *rest):
        msg = message.text.lower()
        msg = msg.replace('?', '')
        now = datetime.now()
        if {'др', 'день рождения'}.intersection(msg.split(' ')):
            resp = vk.users.get(user_id=message.from_id, fields='bdate')[0].get('bdate', None)

            if resp:
                resplit = resp.count('.')
                if resplit == 2:
                    drfull = datetime.strptime(resp, '%d.%m.%Y')
                else:
                    drfull = datetime.strptime(resp, '%d.%m')

                drnow = datetime(now.year, drfull.month, drfull.day)

                if drnow < now:
                    drnow = datetime(now.year + 1, drfull.month, drfull.day)

                left = drnow - now

                ans = f'До Твоего дня рождения: {left.days} дней, {left.seconds // 60 // 60} часов, ' \
                      f'{left.seconds // 60 % 60} минут, {left.seconds % 60} секунд!'
            else:
                ans = 'Я не вижу на твоей странице дату рождения. Либо ты ее не указал, либо страница закрыта'

        elif {'нг', 'новый год'}.intersection(msg.split(' ')):
            ny = datetime(now.year + 1, 1, 1, 0, 0, 0)
            left = ny - now

            ans = f'До Нового года: {left.days} дней, {left.seconds // 60 // 60} часов, ' \
                  f'{left.seconds // 60 % 60} минут, {left.seconds % 60} секунд!'

        else:
            now = now.timestamp()
            now += randint(18000, 315360000)
            ans = datetime.fromtimestamp(now).strftime('%d.%m.%Y в %H:%M')

        answer = ans
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Who:
    keywords = ['кто']
    commands = ['кто']
    attachment = []
    help_name = 'Кто'
    help_content = 'бот выбирает одного из участников беседы'
    help_deep = 'Теперь вы всегда будете знать кто в беседе главный. ' \
                'Для работы команды боту требуются права администратора в беседе. ' \
                'Их может выдать текущий администратор в настройках беседы\n' \
                'Использование: "бот кто молодец?" '

    def answer(self, message, vk, *rest):
        try:
            res = vk.messages.getConversationMembers(peer_id=message.peer_id, group_id=config.my_id)
            profile = choice(res.get('profiles'))
            answer = f"{profile.get('first_name')} {profile.get('last_name')} - " \
                     f"{message.text[message.text.lower().find('кто') + 3:]}"
            answer = answer.replace('?', '')
        except Exception as e:
            if "[917] You don't have access to this chat" in str(e):
                answer = 'Для выполнения этой команды боту нужны права администратора в беседе. Почему? Спросите у ВК'
            else:
                raise

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Why:
    commands = ['почему', 'за что']
    keywords = ['почему', 'почему?', 'что?', "что"]
    attachment = []
    help = ' - '
    help_name = 'Почему'
    help_content = 'бот расскажет'
    help_deep = 'Работает даже без упоминания бота на прямую если разрешены дополнительные команды\n' \
                'Использование: "бла бла почему бла бла" '

    def answer(self, message, vk, *rest):
        answer = choice(texts.why)

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Mayi:
    commands = ['можно мне', 'можно я', 'можно']
    keywords = ['можно']
    attachment = []
    help_name = 'Можно..'
    help_content = 'спроси разрешения у бота'
    help_deep = 'Бот разрешит или не разрешит. Тут уж как повезёт\n' \
                'Использование: "бот можно мне конфетку?" или "бот можно я пойду погуляю?" ' \
                'или "бот безумно можно быть первым?"'

    def answer(self, message, vk, *rest):
        may = choice([True, False])
        r = randint(0, 100)
        if r < 6:
            if may:
                answer = choice(texts.pos_rare)
            else:
                answer = choice(texts.neg_rare)
        else:
            if may:
                answer = choice(texts.may_i_pos)
            else:
                answer = choice(texts.may_i_neg)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Chance:
    commands = ['вероятность', 'егэ', 'шанс']
    keywords = ['вероятность', 'егэ', 'шанс']
    attachment = []
    help_name = 'Вероятность(егэ)'
    help_content = 'показывает случайную вероятность в %'
    help_deep = 'Использование: "бот вероятность что я тоже бот" или "бот как я сдам егэ" '

    def answer(self, message, vk, *rest):
        answer = str(randint(0, 100)) + '%'

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Hello:
    commands = ["привет", "ку", "хай", "здравствуй", 'я вас категорически приветствую']
    keywords = ["привет", "ку", "хай", "здравствуй"]
    attachment = []
    help_name = 'Привет'
    help_content = 'бот с вами поздоровается'
    help_deep = 'Ку! '

    def answer(self, message, vk, *rest):
        answer = choice(self.commands).capitalize()
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Byebye:
    commands = ['всем пока', 'бай', 'пока-пока', 'досвидос', 'до свидания']
    keywords = ['пока', 'бай', 'пока-пока', 'досвидос']
    attachment = []
    help = ' - '
    help_name = 'Пока'
    help_content = 'бот с вами попрощается'
    help_deep = 'Я обязательно придумаю как отличать "Всем пока" от "поехали пока открыто" '

    def answer(self, message, vk, *rest):
        answer = choice(self.commands).capitalize()
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class SweetSleeps:
    commands = ['споки', 'баюбай', 'спокойной', 'спатки', 'спокойной ночи',
                'сладких снов', 'Пусть тебе приснится синий цыплёнок']
    keywords = ['споки', 'баюбай', 'спокойной', 'спатки', 'ночи', 'снов', 'сладких']
    attachment = []
    help_name = 'Спокойной ночи'
    help_content = 'бот с вами попрощается'
    help_deep = 'Сладких снов'

    def answer(self, message, vk, *rest):
        answer = choice(self.commands).capitalize()
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Stickers:
    commands = []
    keywords = []
    attachment = ['sticker']
    help_name = 'Стикер'
    help_content = 'в ответ на стикер бот скинет вам его же если он у него есть'
    help_deep = 'Если вы хотите чтобы он кидал стикер а у него такого нет, ' \
                'можете подарить этот стикерпак админу, должно помочь. Кажется, он пользуется моими'

    def answer(self, message, vk, *rest):
        sticker = (message.attachments[0])['sticker']['sticker_id']
        try:
            bf.sendmessage(vk, peer_id=message.peer_id, sticker_id=sticker)
        except Exception as e:
            config.logger.debug(e)
            if str(e).find("this sticker is not available") != -1:
                if message.peer_id < config.vk_groupchats_id_limit:
                    bf.sendmessage(vk, peer_id=message.peer_id, answer="А у меня нет такого стикера :с")


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Question:
    commands = ['вопрос', 'вопросы', 'поговорить', 'поболтать', 'о чем поговорить']
    keywords = ['вопрос', 'вопросы', 'поговорить', 'поболтать']
    attachment = []
    help = ' - '
    help_name = 'Вопрос'
    help_content = 'задает тему для обсуждения, если поговорить хочется, а придумать о чём не можете'
    help_deep = 'Использование: "бот вопрос" и всей беседкой обсуждаете кто что ответил и почему'

    def answer(self, message, vk, *rest):
        answer = choice(texts.discuss_questions)
        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, mesfromuser=message)


@bf.register(Funclist.standartfunclist)
@bf.addtrigger(bf.standart_trigger)
class Choosen:
    commands = ['или', 'выбор', 'выбери']
    keywords = ['или', 'выбор', 'выбери']
    attachment = []
    help_name = 'Выбор'
    help_content = 'взвешенно и обдуманно выбирает из предложенных вариантов фраз'
    help_deep = 'Выбирает между () или (), или между прикрепленными фотографиями. Если в сообщении нет ни слова "или"' \
                'ни фотографий выберет между словами в сообщении\n' \
                'Использование: "бот выбор" или "бот выбери" и фотографии. ' \
                'Либо "бот выбор 1 или 2 или 3"  или "бот выбери красный черный" '

    def answer(self, message, vk, *rest):
        ans = bf.erase_command(message.text, self.commands[1:]).lower()
        ans = ans.strip()
        sep = ' '
        if 'или' in ans:
            sep = 'или'
        ans = ans.split(sep)

        if ans and ans != ['']:
            answer = choice(ans)
        else:
            answer = 'Не понял из чего выбирать'

        attachment = ''
        if not ans or ans == ['']:
            if message.attachments:
                photo = choice(message.attachments)
                owner_id = photo['photo']['owner_id']
                photo_id = photo['photo']['id']
                if 'access_key' in photo['photo'] and message.peer_id < config.vk_groupchats_id_limit:
                    access_key = photo['photo']['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    answer = 'Мне больше нравится это'
                else:
                    answer = 'Мне больше нравится фотография №' + str(choice(range(len(message.attachments) + 1)))

        bf.sendmessage(vk, peer_id=message.peer_id, answer=answer, attachment=attachment, mesfromuser=message)
