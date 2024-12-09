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
    print(message)
    args = message.text.split()[1:]

    if len(args)!= 1:
        bot.send_message(message.chat.id, "Использование: /wether <город>")
        return
    city = args[0]
    text = weather(city)

    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['wb'])
def wb(message):
    args = message.text.split()[1:]
    if len(args) != 1:
        bot.send_message(message.chat.id, "Использование: /wb <артикул>")
        return


    text = parse(args[0])
    #print(text)
    if text is None:
        print("ERROR(Наверное не правильный артикул)")
        bot.send_message(message.chat.id, "Неверный артикул. Пожалуйста, проверьте и попробуйте снова.")
    elif text == "Misuse detected. Please get in touch, we can come up with a solution for your use case.":
        bot.send_message(message.chat.id, "Проблема с запросом. Пожалуйста, попробуйте позже.")
    else:
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['gpt'])
def gpt(message):
    args = message.text[5:]
    #print(args)
    if len(args) == 0:
        bot.send_message(message.chat.id, "Использование: /gpt <content>")
        return

    wait_message = bot.send_message(message.chat.id, "Подождите, пока ChatGPT завершит обработку информации. Это может занять некоторое время в зависимости от сложности запроса и объема данных. После завершения вы получите ответ.\nСпасибо за ваше терпение!")


    text = GPTFree(args)
    #print(text)
    if text == "Привет! Как я могу помочь тебе сегодня? Если у тебя есть вопросы или нужна информация, просто дай знать!":
        bot.send_message(message.chat.id, "Проблема с запросом. Пожалуйста, попробуйте позже.")
    else:
        bot.send_message(message.chat.id, text)
    bot.delete_message(message.chat.id, wait_message.message_id)
    #bot.send_message(message.chat.id, "test")
    
    
    


@bot.message_handler(commands=['gpt_img'])
def gpt_img(message):
    args = message.text[9:]
    #print(args)
    if len(args) == 0:
        bot.send_message(message.chat.id, "Использование: /gpt_img <content>")
        return

    img_url = GPTFree_img(args)
    #print(img_url)

    bot.send_message(message.chat.id, img_url)


print("bot start1")
bot.polling(non_stop=True)