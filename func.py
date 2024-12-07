import requests
from g4f.client import Client
from config import *



CURS = "https://api.nbrb.by/exrates/rates?periodicity=0"
WETHERAPI = WETHERAPI
client = Client()



def random_duck():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
def random_dog():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
def random_fox():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']




def cours():
    response = requests.get(CURS)
    data = response.json()
    for currency in data:
        if currency['Cur_ID'] == 449:
            grivn = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 431:
            usd = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 451:
            euro = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 452:
            zlotix = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 508:
            uen = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 462:
            uani = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 456:
            rub = currency['Cur_OfficialRate'] / currency['Cur_Scale']
        if currency['Cur_ID'] == 459:
            kzt = currency['Cur_OfficialRate'] / currency['Cur_Scale']
    return grivn, usd, euro, zlotix, uen, uani, rub, kzt


def weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WETHERAPI}"
    #print(url)
    response = requests.get(url)
    data = response.json()
    if data['cod'] != '404':
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        return f"Погода в {city}\nТемпература: {main['temp'] - 273.15:.2f}°C,\nВлажность: {main['humidity']}%,\nСкорость ветра: {wind['speed']*3.6:.2f} км/ч"
    else:
        return "Город не найден"
    


def GPTFree(content):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": {content}}])
    return response.choices[0].message.content