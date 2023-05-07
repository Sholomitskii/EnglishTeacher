import random
import telebot
from telebot import types
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Word, Other_words, create_tables, Command, User, User_word
from dictionary import dict_filling
import requests

TOKEN = '6101502411:AAFg_efFcsJx89QEJDn0iCl_KiOB7yeMadQ'
ya_key = 'dict.1.1.20230417T140531Z.cc7d33edaeb5c3d5.9fab00c3066effbddb6d8fab6869a3386d94b79d'
bot = telebot.TeleBot(TOKEN)

login = 'postgres'
password = '2209fynjy'
db_name = 'learning_english_db'

DSN = f"postgresql://{login}:{password}@localhost:5432/{db_name}"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)

known_users = []
buttons = []
EN_word = ''
RU_word = ''
other_words = []
word_dict_list = []
word_quantity = 0
dictionary1 = []
dictionary2 = []

dict_filling(dictionary1, dictionary2)
session = Session()
session.add_all(dictionary1)
session.add_all(dictionary2)
session.commit()
session.close()

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Привет! Я cмогу тебе помочь! У тебя есть возможность использовать тренажёр как конструктор и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами "Добавить слово" или "Удалить слово". При добавлении нового слова для изучения бот будет автоматически загружать перевод из сервиса "Yandex dictionary".')
    
@bot.message_handler(commands=['start'])
def add_new_user(message):
    global uid
    uid = message.chat.id
    session = Session()
    if uid not in known_users:
        known_users.append(uid)
        new_usr = User(usid = uid)
        session.add(new_usr)
        session.commit()
        q1 = session.query(User).filter(User.usid == uid).all()
        x = q1[0].id
        q = session.query(Word).filter(Word.id <= len(dictionary1))
        for s in q.all():
            wrd = User_word(id_word = s.id, id_user = x)
            session.add(wrd)
        session.commit()
    session.close()
    bot.send_message(message.chat.id, 'Привет! Перед тобой бот-тренажёр, предназначенный для изучения английского языка. Надеюсь, он тебе понравится и принесёт пользу. Введи команду /cards чтобы начать изучать новые слова! Если что-то непонятно, жми /help. Вперёд к новым горизонтам знаний! Приятного обучения!:)')

@bot.message_handler(commands=['cards'])
def start_bot(message):
    word_quantity = session.query(Word).join(User_word).join(User).filter((User.usid == 0)|(User.usid == uid)).count()
    word_id_number = random.randint(0, word_quantity-1)
    oth_wrd_nmb_1 = random.randint(0,38)
    oth_wrd_nmb_2 = random.randint(0,38)
    oth_wrd_nmb_3 = random.randint(0,38)

    global RU_word
    global EN_word
    q = session.query(Word).join(User_word).join(User).filter((User.usid == 0)|(User.usid == uid)).all()
    RU_word = q[word_id_number].russian_word
    EN_word = q[word_id_number].target_word

    w = session.query(Other_words).all()
    oth_wrd_1 = w[oth_wrd_nmb_1].other_word
    oth_wrd_2 = w[oth_wrd_nmb_2].other_word
    oth_wrd_3 = w[oth_wrd_nmb_3].other_word
    
    markup = types.ReplyKeyboardMarkup(row_width=2)

    next_btn = types.KeyboardButton(Command.NEXT_WORD)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)

    target_word_btn = types.KeyboardButton(EN_word)
    global other_words
    other_words = [oth_wrd_1, oth_wrd_2, oth_wrd_3]
    other_words_btns = []
    for word in other_words:
        other_words_btn = types.KeyboardButton(word)
        other_words_btns.append(other_words_btn)
    
    buttons = [target_word_btn] + other_words_btns
    random.shuffle(buttons)
    buttons.extend([delete_word_btn, add_word_btn, next_btn ])
    markup.add(*buttons)
    bot.send_message(message.chat.id, f'Угадай слово {RU_word}', reply_markup=markup)
    
@bot.message_handler(func=lambda message:True, content_types=['text'] )
def message_reply(message):
    global uid
    uid = message.chat.id
    if message.text == EN_word:
        bot.send_message(message.chat.id, 'Верно!')
        start_bot(message)
    elif message.text in other_words: 
        bot.send_message(message.chat.id, 'Попробуй ещё раз, у тебя получится!')
    elif message.text == 'Дальше ->':
        start_bot(message)
    elif message.text == 'Добавить слово (+)':
        get_new_word(message)
    elif message.text == 'Удалить слово (-)':
        get_dlt_word(message)
    
def get_new_word(message):
    new_wrd = bot.send_message(message.chat.id, "Напиши слово на русском языке, которое хочешь добавить ")
    bot.register_next_step_handler(new_wrd, add_word)
    
def add_word(message):
    global new_word
    new_word = message.text
    wrd_list = []
    session = Session()
    q = session.query(Word).all()
    for s in q:
        wrd_list.append(s.russian_word)
    if new_word in wrd_list:
        q1 = session.query(Word).filter(Word.russian_word == new_word)
        q2 = session.query(User).filter(User.usid == uid)
        wrd1 = User_word(id_word = q1.all()[0].id, id_user = q2.all()[0].id)
        session.add(wrd1)
        session.commit()
        word_quantity = session.query(Word).join(User_word).join(User).filter((User.usid == 0)|(User.usid == uid)).count()
        bot.send_message(message.chat.id, f'Слово {new_word} успешно добавлено. Теперь количество изучаемых слов - {word_quantity}')
    else:
        url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={ya_key}&lang=ru-en&text={new_word}'
        response = requests.get(url)
        if len(response.json()['def']) == 0:
            bot.send_message(message.chat.id, 'Такого слова не существует!')
        else:
            translation = requests.get(url).json()['def'][0]['tr'][0]['text'].capitalize()
            session = Session()
            new_wrd = Word(russian_word = new_word, target_word = translation)
            session.add(new_wrd)
            session.commit()
            q = session.query(Word).filter(Word.russian_word == new_word)
            q1 = session.query(User).filter(User.usid == uid)
            wrd1 = User_word(id_word = q.all()[0].id, id_user = q1.all()[0].id)
            session.add(wrd1)
            session.commit()
            word_quantity = session.query(Word).join(User_word).join(User).filter((User.usid == 0)|(User.usid == uid)).count()
            bot.send_message(message.chat.id, f'Слово {new_word} ({translation}) успешно добавлено. Теперь количество изучаемых слов - {word_quantity}')
    session.close()

def get_dlt_word(message):
    del_word = bot.send_message(message.chat.id, "Напиши слово, которое хочешь удалить ")
    bot.register_next_step_handler(del_word, delete_word)

def delete_word(message):
    deleting_word = message.text
    session = Session()
    q = session.query(User_word).join(User).join(Word).filter(Word.russian_word == deleting_word).filter(User.usid == uid).all()
    if len(q) == 0:
        bot.send_message(message.chat.id, 'Этого слова и так нет в твоём словаре :)')
    else:
        x = q[0].id_word
        y = q[0].id_user
        session.query(User_word).filter(User_word.id_word == x).filter(User_word.id_user == y).delete()
        session.commit()
        word_quantity = session.query(Word).join(User_word).join(User).filter((User.usid == 0)|(User.usid == uid)).count()
        bot.send_message(message.chat.id, f'Слово {deleting_word} успешно удалено. Теперь количество изучаемых слов - {word_quantity}')

if __name__ == '__main__':
    bot.polling()

