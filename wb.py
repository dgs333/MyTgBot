#Code https://github.com/Duff89/wb_smart_review

import json
import requests
import re
from g4f.client import Client

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

class WbReview:
    def __init__(self, string: str):
        self.sku = self.get_sku(string=string)
        self.root_id = self.get_root_id(sku=self.sku) if self.sku else None

    @staticmethod
    def get_sku(string: str) -> str:
        """Получение артикула"""
        if "wildberries" in string:
            pattern = r"\d{7,15}"
            sku = re.findall(pattern=pattern, string=string)
            if sku:
                return sku[0]
            else:
                print("Не удалось найти артикул")
                return None  # Возвращаем None, если артикул не найден
        return string
    
    def get_review(self) -> json:
        #!Получение отзывов
        if not self.sku:
            print("Неверный артикул, невозможно получить отзывы")
            return None  # Указываем, что отзывы не получены
        try:
            #print(self.root_id)
            response = requests.get(f'https://feedbacks1.wb.ru/feedbacks/v1/{self.root_id}', headers=HEADERS)
            return response.json()
        except Exception:
            print("Ошибка при получении отзывов")
            return None

    @staticmethod
    def get_root_id(sku: str):
        """Получение id родителя"""
        response = requests.get(
            f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-8144334&spp=30&nm={sku}',
            headers=HEADERS,
        )
        if response.status_code != 200:
            raise Exception("Не удалось определить id родителя")
        try:
            root_id = response.json()["data"]["products"][0]["root"]
            item_name = response.json()["data"]["products"][0]["name"]
            print(item_name)
            return root_id
        except Exception as e:
            print(f"Ошибка при получении id родителя: {e}")
            return None  # Возвращаем None, если не удалось получить id родителя

    def parse(self):
        json_feedbacks = self.get_review()
        if json_feedbacks is None:  # Проверка на успешное получение отзывов
            print("line 68:: ERROR: Не удалось получить отзывы")
            #print(json_feedbacks)
            return []
        try:
            feedbacks = []
            for feedback in json_feedbacks.get("feedbacks", []):
                text = feedback.get("text")
                if text and len(text) < 250:  # Проверяем на пустую строку и длину текста
                    feedbacks.append(text)
            #feedbacks = [feedback for feedback in feedbacks if feedback] #фильтр от пустого текста

            if len(feedbacks) > 100:
                feedbacks = feedbacks[:100]
            #print(feedbacks)
            return feedbacks
        except Exception as e:
            print(f"Ошибка при парсинге отзывов: {e}")
            return []




def ask_gpt_free(feedbacks: list):
    client = Client()
    content = "На основе отзывов очень кратко напиши плюсы и минусы товара. Максимум 3 плюса и 3 минуса. Пиши в формате: Плюсы:\n1. здесь первый плюс\n2. здесь второй плюс\n3. здесь третий плюс Минусы:\n1. здесь первый минус\n2. здесь второй минус\n3. здесь третий минус. Вот отзывы:\n" + f"{feedbacks}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
    )
    return response.choices[0].message.content

def parse(art):
    print(f'артикул - {art}')
    feedbacks = WbReview(string=str(art)).parse()
    if not feedbacks:  # Проверка, если отзывы пусты
        return "ERROR"
    result_gpt = ask_gpt_free(feedbacks=feedbacks)
    return result_gpt