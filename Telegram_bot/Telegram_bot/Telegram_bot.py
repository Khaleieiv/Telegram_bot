import telebot
import config
import random
import string
import datetime
import MySQLdb

from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)

mess = {}       #Тут будем считать сообщения через словарь
mess_time = datetime.date.today()

db = MySQLdb.connect(host = "109.87.9.176",    # localhost
port = 3306,
user = "fooday",         #  username
passwd = "Sergei1234",  #  password
db = "fooday")        # name of the data base
cur = db.cursor()

@bot.message_handler(commands=['start'])

def welcome(message):

    sti = open("D:\static\welcome.jpg", 'rb')
    bot.send_sticker(message.chat.id, sti)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Отримати промокод")
    item2 = types.KeyboardButton("😊 Як справи?")
    item3 = types.KeyboardButton("Допомога")
 
    markup.add(item1, item2, item3)
 
    bot.send_message(message.chat.id, "Ласкаво просимо, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот створений, щоб зберегти ваші грошики.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])

def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Отримати промокод':
             global mess
             global mess_time
             if mess_time != datetime.date.today(): #Если дата не сегодня, сбрасываем все сообщения
                mess = {}
             if message.from_user.id not in mess: #Если пользователь не писал сообщения, то добавляем его ID в словарь и присваиваем 0 сообщений
                mess[message.from_user.id] = 0
             if mess[message.from_user.id] >= 1: #Ставим ограничения на кол-во сообщений
                bot.send_message(message.from_user.id, 'Ваш ліміт вичерпано! \nСпробуйте ' + str(datetime.date.today() + datetime.timedelta(days = 1)))
             else:
                 q = generator_promocode()
                 a = "1"
                 z = random.randrange(5, 10)
                 mess[message.from_user.id] = qty_mess(mess[message.from_user.id])
                 bot.send_message(message.chat.id, q)     
                 bot.send_message(message.chat.id, 'Знижка цього промокодом: ' + str(z) + '%')  
                 cur.execute("INSERT INTO `promocode`(`value`, `active`, `discount_percent`) VALUES (%s, %s, %s)", (q, a, z))
                 db.commit()
                 for result in cur.fetchall():
                    bot.sendMessage(chat_id, result [0])

        elif message.text == '😊 Як справи?':
 
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Добре", callback_data ='good')
            item2 = types.InlineKeyboardButton("Не дуже", callback_data ='bad')
 
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Відмінно сам як?', reply_markup=markup)

        elif message.text == 'Допомога':
            
             keyboard = telebot.types.InlineKeyboardMarkup()  
             keyboard.add(  
             telebot.types.InlineKeyboardButton('Написати менеджеру', url='telegram.me/oleghaleev')) 
  
             bot.send_message(message.chat.id,  
            '1) Кнопка "Допомога" допомагає вам познайомитися з нашим Телеграм-ботом. \n' +
            '2) Натисніть на кнопку "Отримати промокод" для отримання промокодом. \n' +
            '3) Якщо вам стане нудно ви можете поговорити з ботом натиснувши кнопку "Як справи",\n' +
            'Для спілкування з ботом. \n' +
            '4) Якщо виникнуть питання з приводу роботи Телеграм-бота, натиснувши на нижню кнопку, ви можете звязатися з менеджером.',  
             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Я не знаю що відповісти 😢')
 

@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Ось і чудно 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Буває 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хмм",
                reply_markup=None)
 
    except Exception:
        print(repr(e))


def generator_promocode(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def qty_mess(qty):     #Функция для изменения кол-ва сообщений у пользователя
    itog = qty + 1
    return itog

# RUN
bot.polling(none_stop=True)







