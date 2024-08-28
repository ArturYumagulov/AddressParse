import requests

from config.config import YANDEX_URL, YANDEX_API_KEY


def geocode(address: str):
    url = (f"{YANDEX_URL}?"
           f"apikey={YANDEX_API_KEY}"
           f"&geocode={address}"
           f"&format=json"
           f"&lang=ru_RU")

    response = requests.get(url)

    if response.status_code in [400, 403, 429]:
        return {'error': response.json()['message']}
    elif response.status_code == 200:
        return response.json()


if __name__ == '__main__':
    print(geocode("Проспект Мусы Джалиля, 15 Комсомольский район, Набережные Челны, Республика Татарстан, 423800"))
