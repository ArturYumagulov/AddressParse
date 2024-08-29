import datetime

import requests

from config.config import YANDEX_URL, YANDEX_API_KEY, DB
from models.address import ResponseCount


def geocode(address: str, db: DB) -> dict:
    """Функция парсинга адреса из Яндекс"""

    result: dict = {}
    url = (f"{YANDEX_URL}?"
           f"apikey={YANDEX_API_KEY}"
           f"&geocode={address}"
           f"&format=json"
           f"&lang=ru_RU")

    response = requests.get(url)

    count = db.query(ResponseCount).filter(ResponseCount.date == datetime.datetime.utcnow().date()).first()
    count.count += 1
    db.commit()

    if response.status_code in [400, 403, 429]:
        return {'error': response.json()['message']}
    elif response.status_code == 200:
        data = response.json()
        coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
            'pos'].split(' ')
        geocoder_meta_data = \
            data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']
        address_data = geocoder_meta_data['Address']
        result['longitude'] = coordinates[0]
        result['latitude'] = coordinates[1]
        result['request_address'] = address
        result['country_code'] = address_data.get('country_code')
        result['formatted'] = address_data.get('formatted')
        result['zip_code'] = address_data.get('postal_code')
        result['ya_name'] = geocoder_meta_data.get('text')
        for component in address_data['Components']:
            if component['kind'] == "country":
                result['country'] = component['name']
            elif component['kind'] == "province":
                result['province'] = component['name']
            elif component['kind'] == "locality":
                result['city'] = component['name']
            elif component['kind'] == "street":
                result['street'] = component['name']
            elif component['kind'] == "house":
                result['house_number'] = component['name']
            elif component['kind'] == "area":
                result['area'] = component['name']

        return result


if __name__ == '__main__':
    print(geocode("Улица Ефремова, 146а Буинск, Республика Татарстан, 422430"))
