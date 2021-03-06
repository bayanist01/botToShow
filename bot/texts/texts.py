# -*- coding: utf-8 -*-

translit_en_ru = {'N': 'Т', 'd': 'в', 's': 'ы', 'x': 'ч', 'V': 'М', 'k': 'л', '.': 'ю', 'e': 'у', '/': '.', 'G': 'П',
                  'Y': 'Н', 'l': 'д', ';': 'ж',
                  '<': 'Б', 'X': 'Ч', 'Z': 'Я', '[': 'х', 'g': 'п', 'A': 'Ф', 't': 'е', 'M': 'Ь', '$': ';', 'L': 'Д',
                  'Q': 'Й', 'f': 'а', 'H': 'Р',
                  'R': 'К', 'T': 'Е', 'S': 'Ы', ',': 'б', 'O': 'Щ', '"': 'Э', 'P': 'З', 'w': 'ц', 'a': 'ф', ']': 'ъ',
                  'F': 'А', '&': '?', 'J': 'О',
                  'i': 'ш', '^': ':', 'u': 'г', '>': 'Ю', 'U': 'Г', 'b': 'и', 'D': 'В', 'o': 'щ', 'z': 'я', 'p': 'з',
                  'n': 'т', 'c': 'с', ':': 'Ж',
                  "'": 'э', 'I': 'Ш', 'q': 'й', 'v': 'м', 'B': 'И', '`': 'ё', '|': '/', '?': ',', 'h': 'р', 'y': 'н',
                  'm': 'ь', 'K': 'Л', '{': 'Х',
                  '}': 'Ъ', '#': '№', '@': '"', 'C': 'С', 'r': 'к', '~': 'Ё', 'W': 'Ц', 'E': 'У', 'j': 'о'}
translit_ru_en = {'Ч': 'X', 'и': 'b', 'ч': 'x', '/': '|', 'Ф': 'A', 'ц': 'w', 'П': 'G', 'х': '[', 'Г': 'U', '?': '&',
                  'а': 'f', 'О': 'J', 'ж': ';',
                  'Ю': '>', 'Р': 'H', 'Д': 'L', 'Щ': 'O', 'М': 'V', '"': '@', 'я': 'z', 'Ъ': '}', 'у': 'e', 'ф': 'a',
                  'Н': 'Y', 'д': 'l', 'з': 'p',
                  'Т': 'N', 'У': 'E', ',': '?', 'к': 'r', 'ь': 'm', 'Ш': 'I', 'й': 'q', 'Е': 'T', 'И': 'B', 'о': 'j',
                  'т': 'n', 'л': 'k', 'н': 'y',
                  'э': "'", 'З': 'P', 'щ': 'o', 'В': 'D', 'Б': '<', 'Л': 'K', 'Й': 'Q', ';': '$', 'с': 'c', ':': '^',
                  'р': 'h', 'Ы': 'S', '№': '#',
                  'ы': 's', 'Ё': '~', 'К': 'R', '.': '/', 'ъ': ']', 'А': 'F', 'в': 'd', 'п': 'g', 'Ь': 'M', 'г': 'u',
                  'ш': 'i', 'Э': '"', 'м': 'v',
                  'Ц': 'W', 'е': 't', 'Х': '{', 'Я': 'Z', 'б': ',', 'Ж': ':', 'ю': '.', 'С': 'C', 'ё': '`'}
discuss_questions = ['Вы можете пригласить на ужин любого человека. Кого вы выберете?',
                    'Когда вы в последни раз пробовали что-то новое?',
                    'За какие свои дела или навыки вы хотите быть известными?',
                    'Что вы можете сделать сегодня, чего не могли сделать в прошлом году?',
                    'От какой привычки вы хотели бы избавиться?',
                    'Когда вы чувствуете себя собой?',
                    'Что вызывает у вас улыбку?',
                    'Если бы вы могли обрести любую черту характера или способность, что бы вы выбрали?',
                    'Где вы находите вдохновение?',
                    'Как бы вы описали себя в одном предложении?',
                    'Если бы вы могли вернуться в прошлое и что-то изменить, вы бы это сделали?',
                     'Какая у вас любимая песня и почему?',
                     'Если бы вы могли иметь только пять вещей, что бы вы выбрали?',
                     'Какую проблему в мире вы решили бы, если бы могли решить любую проблему?',
                     'Как выглядит ваше путешествие мечты?',
                     'Когда в последний раз вы чувствовали себя счастливыми?',
                     'Чего вам больше всего хотелось бы в данный момент?',
                     'Какую ошибку в жизни вы совершили и чему научились?',
                     'О чем будет ваша книга, если вы её напишете?',
                     'За какие события в жизни вы больше всего благодарны?',
                     'В чём смысл жизни?',
                     'Что нового вы узнали за последнее время?',
                     'Почему людям нравятся злодеи/плохиши?',
                     'В чём сила?']
magic8 = [
    'Бесспорно',
    'Предрешено',
    'Никаких сомнений',
    'Определённо да',
    'Можешь быть уверен в этом',
    'Мне кажется — «да»',
    'Вероятнее всего',
    'Хорошие перспективы',
    'Знаки говорят — «да»',
    'Да',
    'Пока не ясно, попробуй снова',
    'Спроси позже',
    'Лучше не рассказывать',
    'Сейчас нельзя предсказать',
    'Сконцентрируйся и спроси опять',
    'Даже не думай',
    'Мой ответ — «нет»',
    'По моим данным — «нет»',
    'Перспективы не очень хорошие',
    'Весьма сомнительно'
]
why = ('ПОТОМУ ЧТО', 'Так захотела вселенная', 'На все воля божия', 'Согласно пророчеству',
       'Так исторически сложилось', 'Таков мой замысел', 'Во славу сатане', 'Потому что это бесплатно',
       'Потому что каждый год около 200 человек умирают от нападения диких муравьев')
may_i_pos = ('да', 'да, можно', 'а сам(а) как думаешь?', 'можно', 'конечно', 'разумеется можно')
may_i_neg = ('нет', 'нельзя', 'нет, нельзя', 'а сам(а) как думаешь?', 'конечно же нет', 'заняться больше нечем?')
neg_rare = ('а оно тебе надо?', 'и что это тебе даст?', 'вот я в твоем возрасте такой фигней не занимался',
            'спроси позже', 'ой, делай что хочешь', 'можно Машку за ляшку')
pos_rare = ('только шапку одень!', 'только подумай о защите',
            'Делай всё что пожелаешь, сегодня твой день!')
wuw = ('Чем могу помочь?', 'Я тут, жду от тебя команд', 'Список доступных команд можешь узнать, написав мне "помощь"',
       'Человек', 'Что?', 'Я не знаю что на это ответить')
bdate = ['Желаю, чтобы в твоей жизни был только позитив, а рядом находились верные друзья. Пускай тебя всегда переполняет неисчерпаемая энергия для осуществления всех твоих желаний. Пусть вся жизнь будет безоблачной и яркой, а в доме царят уют, мир, любовь и счастье. Если говорить короче, то от всей души желаю тебе прожить жизнь так, как будто побывать в сказке. С днем рождения!',
         'Поздравляю с днем рождения! В этот замечательный день желаю тебе крепкого здоровья, верных и преданных друзей, безграничного счастья, безразмерных доходов, сумасшедшей любви и побольше радостных дней! Хорошего тебе настроения и отличного праздника!',
         'Поздравляю с днем рождения! Желаю, чтобы всё самое лучшее притягивалось в твою жизнь, чтобы тебя ценили, опекали, оберегали, всячески поддерживали и бескорыстно дарили свою любовь. Здоровья тебе, красивой мечты и надежной руки в жизненном путешествии!',
         'Поздравляю с днем рождения. Желаю крупных успехов, крепкого здоровья и надежных друзей. Пусть дом твой будет уютным, теплым и добрым. Пусть никогда не исчезает вдохновение жить, любить, творить и побеждать.',
         'Искренне поздравляю с днем рождения. Желаю осуществить самые желанные мечты. Уюта в доме, на сердце и в душе. Уверенно шагать к своим целям, никогда не сдаваться, служить опорой для старших и образцом для младших, а самое главное, любви, здоровья и поддержки!',
         'Поздравляю с днем рождения! Желаю тебе всегда оставаться таким же бурлящим потоком радости и веселья. Смотри на жизнь с позитивом и целеустремленностью. Не бойся преград, ибо, только преодолевая их, мы осознаем, ради чего стоит жить. Имей много денег, но не поддавайся их соблазнам. Дари тепло и получай его взамен. Пусть друзья всегда придут на помощь, а враги обходят стороной. Пускай удача всегда сопутствует тебе на жизненном пути. Но самое главное — всегда оставайся собой. Еще раз с днем рождения! Всех благ!',
         'Поздравляю с днем рождения! Желаю как можно больше счастливых моментов в жизни, чтобы каждый прожитый миг приносил удовольствие, чтобы близкие люди радовали вас чаще, чем обычно. А также желаю фортуны, повернутой к вам лицом, и чтоб все позитивные мысли, которые вас посещают, сбывались!',
         'Поздравляю с днем рождения! Хотелось бы пожелать много счастья и любви! Пусть невзгоды обходят Вас стороной, и каждый день радует только хорошими событиями. Желаю, чтобы желания непременно осуществились. И, конечно же, чтобы в Вашем сердце жил покой, а Ваша душа ликовала от светлых моментов Вашей жизни. Пусть каждый день приносит только радость и искренних людей в Ваш дом!',
         'С праздником тебя! Этот день только твой. Желаю нескончаемого счастья, удачи, крепкого здоровья, любви, взрывных эмоций. Пусть у тебя всегда будет сила воли и энергия для выполнения любого задания. Любви тебе и уважения со стороны близких, друзей, окружения. Хочу, чтобы в твоей жизни происходила много прекрасных, ярких, огненных событий. С днем рождения!',
         'Пускай твой день рождения будет полон ярких красок, приятных сюрпризов и радужного позитива! Пусть вся твоя жизнь состоит из безграничного счастья и радостных моментов! Желаю искренних улыбок, хороших друзей и взаимной любви!',
         'Поздравляю с чудесным праздником — днем твоего рождения! Пускай каждый новый день начинается с улыбки, шагай по жизни с высоко поднятой головой. Пускай воплощаются в жизнь все твои заветные мечты, реализуются даже самые амбициозные планы. Люби, мечтай, живи на полную!',
         'С днем рождения! Пусть этот день будет полон самых неожиданных и радостных сюрпризов и долгожданных подарков. Пусть рядом с тобой всегда будут самые дорогие люди, верные и надежные друзья. Счастья, любви и добра твоему дому. И пусть тебе улыбнется удача!',
         'Поздравляю тебя от всего сердца с днем именин! Пусть всё задуманное обязательно сбывается! Пусть будет больше поводов для улыбок и радости. Пусть в жизни будут верные друзья. Пусть любовь будет чистой и обязательно взаимной. Здоровье пускай не подводит, а счастье окажется бесконечным! И главное, желаю большого жизненного терпения, всяческих земных благ и всего только самого доброго и прекрасного!',
         'Поздравляю тебя с днем рождения! Желаю тебе много улыбок, от которых становится тепло на душе, побольше замечательных людей, которые не дадут тебе скучать и унывать (а ведь чем больше улыбок — тем больше тепла) и ярких дней, которые будут наполнены положительными эмоциями и счастьем!',
         'С днем рождения! Желаю солнца, тепла, мира, веселья, денег, успехов во всех начинаниях, любви, благополучия, исполнения самых заветных желаний, здоровья и вдохновения! Пусть жизнь дарит много приятных сюрпризов, друзья всегда окружает тебя, а глаза искрятся от счастья!',
         'Желаю, чтобы в твоей душе всегда было равновесие, а гармония с окружающим миром делала твою жизнь легкой и счастливой. Пускай переживания будут только любовными, а страдания и разочарования не присутствуют в твоем сердце вовсе. Желаю, стабильности в жизни, чтобы в ней постоянным были и достаток, и благополучие, и счастье. Пускай сбывается и осуществляется все самое заветное и искренне желаемое. С днем рождения!',
         'С днем рождения! Сегодня день исполнения всех твоих желаний и мечтаний. Желаю тебе самого лучшего настроения, солнечных улыбок от окружающих, и еще ярче улыбки на твоем лице. Хочу пожелать встречать самых лучших людей на твоем пути, и чтобы они всегда были рядом с тобой. Пусть в этот праздник произойдет чудо, которого ты больше всего ждешь!',
         'Поздравляю с праздником рождения! Желаю от жизни получить все: счастья безграничного, здоровья отличного, друзей верных, настроения отменного, достатка круглогодичного и отдыха незабываемого. Пусть глаза всегда сияют радостью, а сердце пылает от любви!',
         'Поздравляю с днем рождения! Хочу пожелать каждый день находить свое счастье, а оно может быть как в простых мелочах, например, в улыбке любимого человека или в кружке вкусного чая, так и в больших свершениях жизни, например, в грандиозной поездке куда-то или в смене твоего имиджа. И неважно, чем именно ты надумаешь заниматься в этот год своей жизни, главное, чтобы тебя уверенно можно было считать счастливым человеком — от самых пяток до кончиков волос! Успехов, любви, творчества, уверенности, удачи и радости!',
         'С днем рождения тебя я поздравляю. Пусть здоровье не покинет, счастье и радость пусть будут всегда и во всем. Желаю тебе бесконечного везения, тепла и мира. Пусть жизнь подарит только позитивные моменты, а ангел хранитель оградит от бед и несчастий.',
         'Поздравляю с днем рождения! Но желать тебе здоровья и счастья, думаю, не стоит, так как все уже давно этого пожелали, и это обязательно будет! Я пожелаю тебе, чтобы у тебя было то, что именно тебе нужно. То, чего хочешь ты и только ты! Ведь только ты знаешь, что тебе нужно для самого главного — для счастья. С днем рождения!',
         'Пусть душа расцветает с каждым днём, пусть сердце питает любовь и радость. Я поздравляю тебя с днем рождения! Желаю крепкого и надежного здоровья, несметного и вечного богатства внутреннего мира, крупной и неизменной удачи на пути, гармонии и самой искренней любви. И пусть каждый миг, каждый день, каждый год приносит только счастье!',
         'Поздравляю с днем рождения! Желаю удачи, счастья, волшебства, успеха во всех начинаниях и продолжениях, верных друзей, любви и солнечного настроения на каждый день. Желаю, чтобы каждое утро начиналось с чашечки чая и радостной улыбки!',
         'Хочу поздравить с днем рожденья и пожелать добра, любви, здоровья, мира, преуспевать во всех начинаниях, а еще чтобы деньги водились. Желаю яркой жизни, чтобы новый день не был похож на предыдущий, счастья в семье, успехов в работе, а в доме — уюта и тепла.',
         'С днем твоего рождения! Я тебе желаю самых изысканных вкусов жизни, самых ярких ощущений, благовидных впечатлений, добрых помыслов и открытой дорожки к счастью. Пусть каждый день дышит по-особенному, принося удовольствие и приятные мелочи. Здоровья тебе, отрадного настроения и воплощения всех твоих целей и желаний.',
         'Пусть этот день рождения тебе принесет столько радости, сколько звезд на ночном небе. Пусть все твои мечты, даже самые невероятные, сбываются, а каждый день жизни будет наполнен счастливыми секундами, незабываемыми мгновениями и очень яркими впечатлениями.',
         'Пускай счастье переполняет твое сердце и каждое мгновение приносит море радости, удачу и сотни приятных сюрпризов! Пускай желания и мечты станут сказочной реальностью! Улыбайся как можно чаще, купайся в любви и получай удовольствие от жизни!',
         'Чудесный, добрый, замечательный и светлый человечек, поздравляю тебя с днем рождения. Желаю, чтобы над тобой не висли серые тучи в жизни, чтобы постоянно в городе твоей души было уютно и красиво, чтобы для беспокойства сердца твоего не было ни одной причины. Чтобы те люди, которыми ты дрожишь, в ответ тебя любили и ценили.',
         'В день твоего рождения хочу пожелать, что бы в жизни было всегда больше счастливых и радостных минут, что бы сердце наполнялось радостью от тёплых и ласковых слов, а рядом находились верные друзья!',
         'Поздравляем Вас с замечательной, значимой датой Вашей судьбы! Желаем Вам успешно идти по жизни, всегда иметь опору и поддержку в лице любящих Вас людей. Пусть крепким будет здоровье, отличным — настроение, хотим, чтобы с лёгкостью реализовывались все Ваши планы. Удачи, везения, любви и много-много счастья!']




i_never = [' Никогда я не прыгал с тарзанки.',
           ' Никогда еще я не ездил на животных.',
           ' Никогда я не путешествовал автостопом больше месяца.',
           ' Никогда меня не арестовывали.',
           ' Никогда я не занимался серфингом.',
           ' Никогда еще меня не убивали током.',
           ' Никогда не получал швов.',
           ' Никогда я не ходил на охоту.',
           ' Никогда я не был веганом.',
           ' Никогда я не воровал в магазине.',
           ' Никогда еще я не терял сознание.',
           ' Никогда я не ломал кость.',
           ' Никогда я не стрелял из пистолета.',
           ' Никогда я не обедал и не разбивал.',
           ' Никогда не ломал зуб.',
           ' Никогда еще я не танцевал в лифте.',
           ' Никогда я не разрушал чужой отпуск.',
           ' Никогда я не прыгал с крыши.',
           ' Никогда меня не ловили за изменой.',
           ' Никогда у меня никогда не было паранормального опыта.',
           ' Никогда меня не ловили в фильмах.',
           ' Я никогда не занимался подводным плаванием.',
           ' Никогда у меня не было дома на дереве.',
           ' Никогда не носил очки с поддельными линзами.',
           ' Я никогда не сидел на диете.',
           ' Я никогда не был на показе мод.',
           ' Я никогда не крал что-нибудь из ресторана.',
           ' Никогда у меня никогда не было плохой аллергической реакции.',
           ' Я никогда не просыпался и не мог двигаться.',
           ' Никогда я не был в ловушке в лифте.',
           ' Я никогда не переписывался четыре часа подряд.',
           ' Я никогда не принимал участие в шоу талантов.',
           ' Никогда я не ходил больше восьми часов подряд.',
           ' Никогда не пытался постричься.',
           ' Я никогда не был в стране в Африке.',
           ' Никогда не думал, что утону.',
           ' Никогда еще я не работал в ресторане быстрого питания.',
           ' Я никогда не влюблялся с первого взгляда.',
           ' Я никогда не пел караоке перед людьми.',
           ' Никогда я не был на телевидении или на радио.',
           ' Я никогда не бодрствую два дня подряд.',
           ' Никогда меня не подбрасывали на американских горках.',
           ' Никогда я случайно не отправлял кого-нибудь в больницу.',
           ' Никогда я не красил волосы в сумасшедший цвет.',
           ' Никогда я не падал в яму глубже, чем мой рост.',
           ' Я никогда не был в стране в Азии.',
           ' Никогда мне не приходилось бежать, чтобы спасти свою жизнь.',
           ' Никогда я не зарабатывал, выступая на улице.',
           ' Я никогда не видел аллигатора или крокодила в дикой природе.',
           ' Никогда я полностью не забывал свои линии в пьесе.',
           ' Никогда еще меня не устраивали вечеринки-сюрпризы.',
           ' Никогда я случайно не говорил «Я тебя люблю» кому-то.',
           ' Никогда я не нажимал кнопку отправить, а потом сразу об этом пожалел.',
           ' Никогда я не был влюблен в родителя друга.',
           ' Никогда мне не приходилось, чтобы кто-то ударил меня по лицу.',
           ' Никогда я никогда не плакал на публике из-за песни.',
           ' Я никогда не читал целый роман за один день.',
           ' Никогда еще я никого не заставлял делать татуировки или пирсинг.',
           ' Никогда еще я не просматривал чужие телефоны без их разрешения.',
           ' Никогда у меня никогда не было физической ссоры с моим лучшим другом.',
           ' Я никогда не бросал что-то в экран телевизора или компьютера.',
           ' Я никогда не выходил с фильма, потому что это было плохо.',
           ' Никогда еще я не был настолько загорелым, что не мог носить рубашку.',
           ' Никогда на меня не кричал клиент на моей работе.',
           ' Никогда я не брал еду из мусорного ведра и не ел ее.',
           ' Я никогда не плакал / флиртовал, выходя из талона на превышение скорости.',
           ' Никогда еще я не был в неловком видео, которое было загружено на YouTube.',
           ' Я никогда не пробирался через ванную или спальню друга без его ведома.',
           ' Никогда я специально не поджигал свои или чужие волосы в огне.',
           ' Никогда у меня никогда не было плохого падения, потому что я гулял и переписывался.',
           ' Я никогда не проводил ночь в лесу без крова.',
           ' Я никогда не ломал что-то в доме друга, а потом не говорил им.',
           ' Никогда я не был без тепла зимой или без кондиционера летом.',
           ' Никогда еще я не работал с кем-то, кого я ненавидел с пылающим огнем тысячи солнц.',
           ' Я никогда не ранил себя, пытаясь произвести впечатление на девушку или мальчика, которые меня интересовали.',
           ' Я никогда не лгал о смерти члена семьи в качестве предлога, чтобы уйти от каких-либо действий.']

true = '''Сколько тебе лет?
Во сколько лет был твой “первый раз”?
Какое блюдо ты ненавидишь?
За какое свое действие тебе до сих пор стыдно?
Есть ли человек среди нас, который тебе нравится, как парень (девушка)?
Какая часть тела у тебя сама привлекательная?
Кого бы ты выбрал(а) из этой компании на безлюдный остров? (Только противоположного пола)
Каким было твое первое свидание?
Где и каким был твой первый поцелуй?
Ты вспоминаешь бывшего (бывшую) с мыслями “вот если бы сейчас…”?
Сколько ты зарабатываешь в месяц?
С кого из своего окружения ты берешь пример? 1-3 человека
Что больше всего раздражает в людях?
Кто из здесь присутствующих тебя напрягает?
Какой твой поступок ты считаешь безумным или бездумным?
Что ты сделал(а) бы, если бы стал(а) парнем (девушкой) на один день?
Чьи мысли из нашей компании ты хотел (а) бы прочитать?
Твои 3 вредные привычки?
Твое любимое животное?
О чем чаще всего обманываешь (большая или маленькая ложь)?
Во сколько чаще всего ложишься спать?
За какой фильм тебе было стыдно даже перед собой?
Любимый сериал и почему именно он?
Какая разница в возрасте тебя не остановила бы для отношений?
Какой алкоголь любишь больше всего?
У тебя есть кредит и на какую сумму?
Тебя ставили в детстве в угол? Наказывали ремнем?
Что ты думаешь про соседа справа? Внешность и характер.
Что выберешь: iPhone или Андроид смартфон?
Пробовал (а) курить? Если куришь – хотелось бы бросить?
На что бы ты не смог(ла) пойти ради любимого человека?
На что потратил(а) бы миллион долларов, если на это были бы сутки?
Кто из игроков больше похож на идеал для хороших отношений?
Что или кто тебе чаще снится?
Ты диктатор: какой будет твой первый закон?
Твоя “скрытая” фантазия, какая она?
У тебя был “кекс” по дружбе?
Ты встречался (лась) с бывшим (ей)?
Любишь мультики? Какие любимые?
Грызешь ногти?
Ковыряешь ли в носу?
Что отпугивает тебя на свидании?
Когда спишь, ты храпишь?
Чего ты боишься больше всего?
Идеальный возраст для создания семьи на твой взгляд?
Кого бы ты поцеловал (а) прямо здесь и сейчас?
Ходил(а) по маленькому в бассейн или в море?
Самый запомнившийся подарок тебе?
Прятал (а) дырку в носке (колготах)?
Твой самый “жаркий” сон, о чем он?
Ты ревнивый человек?
Простил(а) бы измену любимого человека?
Твоя самая любимая вещь в твоем гардеробе: какая она?'''.split('\n')

do = '''Станцуй в течении 60 секунд под песню, которую выбрали тебе друзья.
Выпей стакан воды (0,5) одним разом.
Поцелуй случайного прохожего (противоположного пола. Если нужно – уговаривай).
Прочитай стишок, как в детстве, на стульчике с выражением.
Погавкай громко 5-8 раз на прохожего (в кафе или на улице).
Подари любую вещь из своей сумки или кармана соседу левее от тебя.
Два человека из нашей компании рисуют тебе усы ручкой, которые ты не смываешь в течении 2-ух часов.
Покажи всем краешек своего нижнего белья.
Выверни наизнанку свою одежду и не переодевайся до конца игры.
Сделай 5 минут массажа соседу левее или правее от тебя. Во время процесса все продолжают играть.
Съешь большой сникерс за 60 секунд. Если не успеешь – купи такой же соседям справа и слева.
Попробуй спародировать любого игрока (противоположного пола).
Сделай шарфик из туалетной бумаги. Выйди на улицу и спроси 2-ух прохожих, как пройти на остановку.
Завяжите игроку глаза, раскрутите вокруг себя. Затем игрок должен на ощупь найти и угадать любого игрока в комнате.
Дай каждому сидящему кличку.
Попроси у прохожих денег на пиво. Просить нужно до момента, когда кто-то даст хоть 1 монету или первых 5 прохожих.
“Прожарь” игрока напротив: в шуточной, саркастичной манере высмей его недостатки и плюсы.
Лизни кусочек мыла.
Прочитай последнее смс в твоем телефоне.
Прочитай последние 3 сообщения в Директе Instagram.
Пригласи на свидание любого из присутствующих. Это не должно быть шуточное свидание. Ты точно должен (должна) на него пойти, если человек согласиться.
Покажи всем свой голый живот.
Поцелуй каждого игрока противоположного пола крепко в губы (только двое могут отказать тебе в этом).
Съешь что-то не используя руки. Если это “что-то” нужно достать, ты также не должен использовать для этого руки.
Позвони одному из родителей и скажи, как ты любишь его на громкой связи. Нельзя говорить, что ты в компании или ты на громкой.
Игрок напротив тебя хочет приготовить тебе коктейль, а ты с удовольствием его выпьешь. Использовать можно любые съедобные или жидкие  продукты. Например, коктейль из морепродуктов с сладким мороженным и алкоголем.
Набери любой номер наугад и если попался человек противоположного пола, расскажи, как ты скучаешь. Если попался того же пола, что и ты – тебе повезло, игра продолжается.
Игрок напротив тебя нарисует тебе монобровь. Затем ты выложишь фото с монобровью в свой Instagram. Нельзя подписывать чем-то, что намекнет на твое задание или вашу игру.
Станцуй на коленях в течении 60 секунд перед первым игроком противоположного пола слева от тебя.
Отнеси на себе любого игрока в туалет.
Теперь ты в течении 20 минут все что произносишь, делаешь это музыкально. Т.е. тебе нужно пропеть все, что хочешь или захочешь сказать.
Высунь язык и не засовывая его обратно признайся в любви любому игроку противоположного пола.
Первый игрок противоположного пола слева от тебя заправит твою рубашку (блузку, кофту, свитер, футболку) тебе в трусы. При этом ты держишь руки вверх.
Тебе придется отжаться 15 раз от пола. Удачи.
На 5 минут ты стал(а) писателем. Тебе нужно придумать короткую историю в которой нужно использовать следующие слова без склонений: люблю, кекс, жарить, имеет значение, лифчик, аптека, пончик.
Тебе нужно каждому игроку сказать честный комплимент.
Когда следующие 3 игрока будут говорить, следи за их словами. При каждом услышанном “я” или “и” – ты должен (должна) громко гавкнуть.
Сделай массаж стопы ног для игрока справа или слева от тебя на твой выбор.
Спародируй любого известного актера или певца (певицы) так, чтобы догадались о ком речь.
Тебе придется съесть лимон целиком со шкуркой. Удачи.
Сними брюки (штаны, юбку и т.д.). Если играете в кафе, можно укрыть ноги полотенцем. Оставайся в таком прикиде до конца игры.
Проведи душевную беседу на тему любви и отношений со стулом. Разговаривай так, буд-то стул тебя понимает.
Нужны 3 человека: слева, справа и напротив тебя. Они нарисуют что-то у тебя на лбу. Ты идешь в магазин за газировкой. Посмотреть на рисунок можно только принеся газировку на стол.
Укуси каждого игрока противоположного пола за любую часть тела. При этом нельзя повторяться.
Тебе повезло! Загадай действие любому игроку. Все, что придет на ум.
Все игроки вдруг захотели увидеть тебя пьяным (пьяной). Изобрази новогоднюю речь в таком состоянии.
Сделать селфи с 5-ю незнакомыми людьми на улице (или в кафе).
Предложите и почистите обувь прохожему (если в кафе – просто незнакомцу). Задание выполнено, когда вы почистите обувь.
Понюхай каждого игрока противоположного пола и скажи чем пахнет на твой взгляд.
Собери подписи незнакомцев в петиции по защите прав бешеных улиток. На листке А4 пишем заголовок: “Я поддерживаю инициативу по защите бешеных улиток в нашем городе”. Дальше в столбик собрать 10 подписей.
В аптеке купить през.вативы с фразой “Подскажите, а какие больше подходят для дедушек? Мне в дом престарелых попросили купить”.
Крепко обнять 5 прохожих противоположного пола. Удачи.
Подарить цветок любому игроку противоположного пола.'''.split('\n')

agree = [
    'Полностью с тобой согласен',
    'Бесспорно',
    'Точно так',
    'Да, это так',
    'Звучит убедительно'
]

atroll = {
    'я':'ты',
    'меня':'тебя',
    'обо мне':'о тебе',
    'мной':'тобой',
    'мною':'тобою',
    'мне':'тебе',
    'мы':'вы',
    'нас':'вас',
    'нам':'вам',
    'нами':'вами',
    'мой':'твой',
    'моё':'твоё',
    'моего':'твоего',
    'моему':'твоему',
    'моим':'твоим',
    'моём':'твоём',
    'мое':'твое',
    'моя':'твоя',
    'моей':'твоей',
    'мою':'твою',
    'мои':'твои',
    'моих':'твоих',
    'моими':'твоими'}
