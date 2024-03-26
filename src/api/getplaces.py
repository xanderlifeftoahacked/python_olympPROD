from os import getenv
from typing import List, Tuple

from api.httpxclient import client
from templates.travel_helper import Templates, TemplatesGen

FORSQUARE_TOKEN = str(getenv('FORSQUARE_TOKEN'))
YANDEX_ORG_TOKEN = 'dfac9118-8857-4bac-a6f4-099871519e81'


def get_url_interesting_places(lat: float, lon: float):
    return ('https://api.foursquare.com/v3/places/search?'
            f'll={lat},{lon}&radius=10000&categories=16000%2C10000&'
            'fields=name%2Clocation%2Cdistance%2Cdescription%2Chours%2Cgeocodes&'
            'sort=POPULARITY&limit=10')


def get_url_cafes(lat: float, lon: float):
    return ('https://search-maps.yandex.ru/v1/?text=cafe&'
            'type=biz&lang=ru_RU&results=50&'
            f'll={lon},{lat}&spn=0.1,0.1&'
            f'apikey={YANDEX_ORG_TOKEN}')


async def get_cafes(lat: float, lon: float) -> Tuple[str, List]:
    response = await client.get(url=get_url_cafes(lat, lon))
    if response.status_code != 200 or not response.json():
        return Templates.OPENTRIP_ERROR.value, []
    features = response.json()['features']

    locs = []
    ans = ''
    counter = 0
    for feature in features:
        coords = (feature['geometry']['coordinates'][1],
                  feature['geometry']['coordinates'][0])
        if not 'CompanyMetaData' in feature['properties']:
            continue

        data = feature['properties']['CompanyMetaData']

        if 'Hours' not in data or 'address' not in data:
            continue

        counter += 1
        if counter > 10:
            break
        url = data['url'] if 'url' in data else ''
        hours = data['Hours']['text']
        name = data['name']
        address = data['address']

        ans += TemplatesGen.cafe(name, address, url, hours, counter)
        locs.append(coords)

    return ans, locs


async def get_interesting_places(lat: float, lon: float) -> Tuple[str, List]:
    headers = {
        'accept': 'application/json',
        'Accept-Language': 'ru',
        'Authorization': FORSQUARE_TOKEN
    }

    response = await client.get(url=get_url_interesting_places(lat, lon), headers=headers)
    if response.status_code != 200 or not response.json():
        return Templates.OPENTRIP_ERROR.value, []
    response = response.json()

    if not response['results']:
        return Templates.NO_INTERESTING.value, []
    ans = ''
    places = []
    for index, place in enumerate(response['results'], 1):
        if 'description' in place:
            description = place['description']
        else:
            description = ''
        ans += TemplatesGen.place(is_open=place['hours']['open_now'],
                                  name=place['name'],
                                  description=description,
                                  address=place['location']['formatted_address'],
                                  distance=place['distance'], index=index)
        places.append((place['geocodes']['main']['latitude'],
                       place['geocodes']['main']['longitude']))
    return ans, places
