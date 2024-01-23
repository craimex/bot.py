import telebot
from telebot import types

token = "6526772250:AAGPy8XUSGUtPZ7AO8VdFaDJ6NBTvwQQJkY"
bot = telebot.TeleBot(token)

player_states = {}


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.location = "Деревня"
        self.character = None

# Функция для обработки команды /choose_character
@bot.message_handler(commands=['choose_character'])
def choose_character(message):
    if message.chat.id not in player_states:
        bot.send_message(message.chat.id, "Сначала начните игру с помощью команды /start.")
    else:
        player = player_states[message.chat.id]
        if player.character is not None:
            bot.send_message(message.chat.id, "Вы уже выбрали персонажа.")
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1)
            button1 = types.KeyboardButton("Mage")
            button2 = types.KeyboardButton("Warrior")
            button3 = types.KeyboardButton("Thief")
            keyboard.add(button1, button2, button3)
            bot.send_message(message.chat.id, "Выберите своего персонажа:", reply_markup=keyboard)

# Функция для обработки ответов игрока на выбор персонажа
@bot.message_handler(func=lambda message: message.text in ["Mage", "Warrior", "Thief"])
def handle_character_choice(message):
    player = player_states[message.chat.id]
    if player.character is None:
        player.character = message.text
        bot.send_message(message.chat.id, f"Вы выбрали персонажа: {player.character}. Теперь вы можете начать игру с помощью команды /start.")
    if player.character == "Thief":
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/g5BcrD-eAZ8qgg")
    elif player.character == "Mage":
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/urTBbLQ0WLuhFQ")
    elif player.character == "Warrior":
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/w0Ek3uTr-g4kGg")
    else:
        bot.send_message(message.chat.id, "Вы уже выбрали персонажа.")

# Обновленная функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in player_states:
        player_states[message.chat.id] = Player(message.from_user.first_name)
        bot.send_message(message.chat.id, "Привет! Добро пожаловать в игру. Выберите своего персонажа с помощью команды /choose_character.")
    else:
        bot.send_message(message.chat.id, "Вы находитесь в мире людей и ёкай(демоны).Главный герой - избранный. Он на половину ёкай и на половину человек. Великий ёкай Отакемару пробудился и ваша задача остановить его. Введите /location, чтобы продолжить.")

# Функция для обработки команды /location
@bot.message_handler(commands=['location'])
def show_location(message):
    player = player_states[message.chat.id]
    location_description = "Вы находитесь в " + player.location + ". Что вы хотите сделать?"
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    if player.location == "Деревня":
        button1 = types.KeyboardButton("Исследовать")
        button2 = types.KeyboardButton("Перейти в поле")
        button3 = types.KeyboardButton("Получить информацию о Деревне")
        keyboard.add(button1, button2, button3)
    elif player.location == "Поле":
        button1 = types.KeyboardButton("Тренироваться")
        button2 = types.KeyboardButton("Вернуться в деревню")
        button3 = types.KeyboardButton("Перейти в лагерь")
        button4 = types.KeyboardButton("Получить информацию о Поле")
        keyboard.add(button1, button2, button3, button4)
    elif player.location == "Лагерь":
        button1 = types.KeyboardButton("Напасть на лидера")
        button2 = types.KeyboardButton("Получить информацию о Лагере")
        button3 = types.KeyboardButton("Бежать в замок Химедзи")
        keyboard.add(button1, button2, button3)
    elif player.location == "Замок":
        button1 = types.KeyboardButton("Взгялнуть вокруг")
        button2 = types.KeyboardButton("Получить информацию о Замке")
        button3 = types.KeyboardButton("Напасть на Осакабэ Химэ")
        keyboard.add(button1, button2, button3)
    elif player.location == "Храм":
        button1 = types.KeyboardButton("Посмотреть вокруг")
        button2 = types.KeyboardButton("Получить информацию о Храме")
        button3 = types.KeyboardButton("Напасть на Шутена Додзи")
        keyboard.add(button1, button2, button3)
    elif player.location == "Храм Бёдо-ин":
        button1 = types.KeyboardButton("Идти на свет вашего медальона")
        button2 = types.KeyboardButton("Получить информацию о Храме Бёдо-ин")
        button3 = types.KeyboardButton("Отправиться в сон Отакемару")
        keyboard.add(button1, button2, button3)
    elif player.location == "Сон Отакемару":
        button1 = types.KeyboardButton("Сразиться с Отакемару")
        keyboard.add(button1)


    bot.send_message(message.chat.id, location_description, reply_markup=keyboard)

@bot.message_handler(commands=['end'])
def end_game(message):
    if message.chat.id in player_states:
        del player_states[message.chat.id]
        bot.send_message(message.chat.id, "Игра завершена. Ваш прогресс был удалён. Нажмите /start для новой игры.")
    else:
        bot.send_message(message.chat.id, "Игра ещё не начата.")

# Функция для обработки ответов игрока
@bot.message_handler(func=lambda message: True)
def handle_player_action(message):
    player = player_states[message.chat.id]
    if message.text == "Исследовать":
        if player.location == "Деревня":
            bot.send_message(message.chat.id, "Вы нашли немного золота!")
    elif message.text == "Получить информацию о Деревне":
        if player.location == "Деревня":
            bot.send_message(message.chat.id, "Деревня - это единственное место не захваченное ёкай. Здесь вы можете свободно путешествовать и смотреть на пейзажи этого великолепного мира.")
            bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/n2Ulitu5B3HMtQ")
    elif message.text == "Перейти в поле":
        player.location = "Поле"
        bot.send_message(message.chat.id, "Вы перешли в поле. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/Pt4GOQsT9KtYSw")
    elif message.text == "Получить информацию о Поле":
        if player.location == "Поле":
            bot.send_message(message.chat.id, "В своё время здесь находился огромный сад, в котором, по словам стариков, невероятно красиво цвела сакура. Однако несколько десятков лет назад армия ёкай во главе с Шутеном Додзи сожгла сад, убив всех, кто находился рядом. Теперь поле лишь огромная пустошь, где изредка можно сразиться со слабыми ёкай.")
            bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/_f_faBqJhrTO9Q")
    elif message.text == "Тренироваться" and player.location == "Поле":
        bot.send_message(message.chat.id, "Вы повысили свои основные характеристики убив несколько Гаки.")
    elif message.text == "Вернуться в деревню" and player.location == "Поле":
        player.location = "Деревня"
        bot.send_message(message.chat.id, "Вы вернулись в деревню. Нажмите /location")
    elif message.text == "Перейти в лагерь":
        player.location = "Лагерь"
        bot.send_message(message.chat.id, "Вы перешли в лагерь. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/RKCr461zb9QHOQ")
    elif message.text == "Получить информацию о Лагере":
        bot.send_message(message.chat.id, "Лагерь - это бывшая деревня, захваченная ёкай слабого уровня во главе с более сильным демоном.")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/FkrmrxjinK6b_Q")
    elif message.text == "Бежать в замок Химедзи":
        player.location = "Замок"
        bot.send_message(message.chat.id, "Вы перешли в замок Химедзи. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/c_OnTDFzLKP_BQ")
    elif message.text == "Взгялнуть вокруг":
        bot.send_message(message.chat.id, "Вокруг лишь тишина и спокойствие. Это настораживает")
    elif message.text == "Получить информацию о Замке":
        bot.send_message(message.chat.id, "Замок Химедзи - древнее сооружение ёкай. Здесь живет один из сильнейших демонов, ёкай по имени Осакабэ Химэ. Она может управлять духами и читать мысли слабых людей, тем самым подчиняя их.")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/XKY1W6SppAh_eg")
    elif message.text == "Напасть на Осакабэ Химэ" and player.location == "Замок" and player.character == "Mage":
        bot.send_message(message.chat.id, "Благодаря своим знаниям вам удаётся понять принцип рпбоы сил госпожи. Подчинение зависит от вашего уровня магии, у кого выше уровень магии тот и подчиняет другого. В поединке магии вы оказались сильнее и приказали Осакабэ Химэ убить себя.")
        player.location = "Храм Бёдо-ин"
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
    elif message.text == "Напасть на Осакабэ Химэ" and player.location == "Замок" and player.character == "Warrior":
        bot.send_message(message.chat.id, "По неведомой причине Осакабэ Химэ подчиняет вас. Казалось бы на этом сражение окончено, но ваша сила воли невероятна. Вам удаётся избавиться от контроля и точным ударом вы убиваете демона.")
        player.location = "Храм Бёдо-ин"
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
    elif message.text == "Напасть на Осакабэ Химэ" and player.location == "Замок" and player.character == "Thief":
        bot.send_message(message.chat.id, "Благодаря вашей невидимости демона удаётся застать врасплох. Вы наносите быстрый и точный удар, лишив Осахабэ Химэ глаз. Она не может видеть вас и вы с лёгкостью заканчиваете поединок.")
        player.location = "Храм Бёдо-ин"
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
    elif message.text == "Напасть на лидера" and player.location == "Лагерь" and player.character == "Mage":
        bot.send_message(message.chat.id, "Вы превратились в одного из ёкай. Пробравшись поближе к лидеру вы использовали ваше сильнейшее заклинание: Луч света. Лидер повержен, а его слуги бегут. Лагерь освобожден, все жители благодарны вам.")
        player.location = "Храм"
        bot.send_message(message.chat.id, "Вы перешли в храм. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/MuFJy1juiPmAaw")
    elif message.text == "Напасть на лидера" and player.location == "Лагерь" and player.character == "Warrior":
        bot.send_message(message.chat.id, "Вы невероятно сильны и под вашим мечом оказываются все вражеские существа. Лагерь освобожден, все жители благодарны вам.")
        player.location = "Храм"
        bot.send_message(message.chat.id, "Вы перешли в храм. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/MuFJy1juiPmAaw")
    elif message.text == "Напасть на лидера" and player.location == "Лагерь" and player.character == "Thief":
        bot.send_message(message.chat.id, "Вас очень тяжело заметить. Не издавая громких звуков вы убиваете ёкай ро одному. Участи не удается избежать даже их лидеру. Лагерь освобожден, все жители благодарны вам. ")
        player.location = "Храм"
        bot.send_message(message.chat.id, "Вы перешли в храм. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/MuFJy1juiPmAaw")
    elif message.text == "Посмотреть вокруг":
        bot.send_message(message.chat.id, "Вы смотрите по сторонам и видете небольшую, но очень сильную армию ёкай. Среди них есть и сам Шутен Додзи.")
    elif message.text == "Получить информацию о Храме":
        bot.send_message(message.chat.id, "Храм Шутена Додзи - это жилище великого ёкай. С детства демон был одарён огромной силой и с возрастом только развивал её. В какой-то момент Шутен Додзи стал настолько силён, что возглавил большую армию ёкай. Среди демонов ему практически не было равных. Однако вёл себя ёкай не очень серьёзно. Он любил танцы и выпивку. Возможно это сыграет с ним злую шутку.")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oWAOHOiDf8eaVg")
    elif message.text == "Напасть на Шутена Додзи" and player.location == "Храм" and player.character == "Mage":
        bot.send_message(message.chat.id, "Как и раньше вы превращаетесь в одного из ёкай и втираетесь в доверии к Шутену Додзи. Зная историю вы вспоминаете, что демон не может устоять перед выпивкой. Отравив напиток вы предложили всем отведать его. Демоны ослабли и в скором времени на помощь пришла армия из ранее освобождённого лагеря. Храм захвачен, а великий демон Шутен Додзи был отравлен вновь :)")
        player.location = "Храм Бёдо-ин"
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
    elif message.text == "Напасть на Шутена Додзи" and player.location == "Храм" and player.character == "Warrior":
        bot.send_message(message.chat.id, "Вы предложили Шутену Додзи честный поединок один на один. Предводитель ёкай согласен. В долгой и тяжёлой битве вы одерживаете победу, уничтожив склянку с силой демона. Шутен Додзи повержен, а храм в скором времени был захвачен людьми из лагеря. Вы перешли в храм Бёдо-ин.")
        player.location = "Храм Бёдо-ин"
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
    elif message.text == "Напасть на Шутена Додзи" and player.location == "Храм" and player.character == "Thief":
        bot.send_message(message.chat.id, "С помощью навыков невидимости вам удаётся отравить напитки. Все ёкай мертвы, но Шутен Додзи продолжает стоять на ногах, он лишь ослаблен. Похоже ваших магических навыков не хватило. Однако не смтря на это, опьянённый Шутен Додзи не в силах успеть за вами. Вы ловко уворачиваетесь и наносите ответные удары и в конце концов демон терпит поражение. Храм захвачен, скоро его заселят люди.")
        player.location = "Храм Бёдо-ин"
        bot.send_message(message.chat.id, "Вы перешли в храм Бёдо-ин. Нажмите /location")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/oD4Erk6Ilgqtaw")
    elif message.text == "Идти на свет вашего медальона":
        bot.send_message(message.chat.id, "Вы приходите к странной стене. Около неё находится лезвие чего-то острого. Интуитивно вы пробуете соединить ваш медальон с лезвием. Вспышка яркого света и вы получаете легендарный клинок-убийцу ёкай. Вы можете сразиться с Отакемару.")
        player.location = "Сон Отакемару"
        bot.send_message(message.chat.id, "Вы попали в сон Отакемару. Нажмите /location")
    elif message.text == "Получить информацию о Храме Бёдо-ин":
        bot.send_message(message.chat.id, "Храм Бёдо-ин - это место где был запечатан легендарный клинок-убийца ёкай, которым однажды был побеждён Отакемару. Отакемару - кидзин, настолько мощный ёкай, что его считают и демоном и богом. Он способен вызывать бури, затмевающие целые горы, а так же может принимать облики других существ.")
        bot.send_photo(message.chat.id, photo="https://disk.yandex.ru/i/ZdiblVI4PibUvQ")
    elif message.text == "Отправиться в сон Отакемару" and player.location == "Храм Бёдо-ин":
        bot.send_message(message.chat.id, "Вы отчаянно сражаетесь, и доводите Отакемару до предела, однако вам не хватает сил добить ёкай. Обычное оружие не может убить короля ёкай. Вы погибли. Введите /end")
    elif message.text == "Сразиться с Отакемару" and player.location == "Сон Отакемару":
        bot.send_message(message.chat.id,
                         "В поединке сошлись два сильнейших воина Японии. Казалось битва не закончится никогда, но в в конце концов ваши силы заканчиваются. Вы решаете вложить оставшуюся энергию в последнюю комбинацию атак. Ваши мечи схлеснулись, но Отакемару не может вынести свет клинка-убийцы. Вам удаётся одолеть величайшего из всех ёкай. Человечество спасено. Введите /end")
        pass
    else:
        bot.send_message(message.chat.id, "Неверный выбор. Пожалуйста, выберите действие из списка.")


bot.polling()