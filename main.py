from telebot import TeleBot, types
from func import *
from wb import parse
from config import *


bot = TeleBot(token=TOKENTG)





@bot.message_handler(commands=['start'])
def start(message):
    print(f"Ник - {message.from_user.username}")

@bot.message_handler(commands=['tts'])
def tts(message):
    bot.send_message(message.chat.id, text="Создатель UTENA")


#!----------------------------------------------------------------

@bot.message_handler(commands=['duck'])
def random_d(message):
    bot.send_message(message.chat.id, random_duck())
@bot.message_handler(commands=['dog'])
def random_do(message):
    bot.send_message(message.chat.id, random_dog())
@bot.message_handler(commands=['fox'])
def random_f(message):
    bot.send_message(message.chat.id, random_fox())
#!----------------------------------------------------------------


@bot.message_handler(commands=['curs'])
def curs(message):
    print(f"Ник - {message.from_user.username}")
    args = message.text.split()[1:]

    if len(args)!= 1:
        bot.send_message(message.chat.id, "Использование: /curs <количество>")
        return
    
    try:
        grivn, usd, euro, zlotix, uen, uani, rub, kzt = cours() 
        #vault = args[0]
        count = float(args[0])

        text = f"""
        {count} bun в
--------------------------------------------
{count / grivn:.2f} гривен,
{count / usd:.2f} долларов США,
{count / euro:.2f} евро,
{count / zlotix:.2f} злотых,
{count / uen:.2f} йен,
{count / uani:.2f} юаней,
{count / rub:.2f} рублей,
{count / kzt:.2f} тенге.
Национальный банк Республики Беларусь
        """
        bot.send_message(message.chat.id, text)

    except ValueError:
       bot.reply_to(message, "Пожалуйста, введите данные\n(Использование: /curs <количество>)")


@bot.message_handler(commands=['weather'])
def weather(message):
    print(f"Ник - {message.from_user.username}")
    args = message.text.split()[1:]

    if len(args)!= 1:
        bot.send_message(message.chat.id, "Использование: /wether <город>")
        return
    city = args[0]
    text = weather(city)

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['gpt'])
def gpt(message):
    print(f"Ник - {message.from_user.username}")
    args = message.text.split()[1:]
    if len(args)!= 1:
        bot.send_message(message.chat.id, "Использование: /gpt <content>")
        return

    text = GPTFree(args)
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['wb'])
def wb(message):
    print(f"Ник - {message.from_user.username}")
    args = message.text.split()[1:]
    if len(args)!= 1:
        bot.send_message(message.chat.id, "Использование: /wb <артикул>")
        return

    
    text = parse(args[0])
    if text != "Misuse detected. Please get in touch, we can come up with a solution for your use case.":
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Проблема с запросом. Пожалуйста, попробуйте позже.")

print("bot start1")
bot.polling(non_stop=True)