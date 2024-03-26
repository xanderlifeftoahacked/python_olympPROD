from os import getenv
from typing import List, Tuple

from api.httpxclient import client
from templates.travel_helper import Templates, TemplatesGen

AMADEUS_TOKEN = str(getenv('AMADEUS_TOKEN'))
AMADEUS_SECRET = str(getenv('AMADEUS_SECRET'))


async def request_hotels_list(lat: float, lon: float, token: str):
    url = 'https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'latitude': lat,
        'longitude': lon,
        'radius': 4,
    }

    return await client.get(url, params=params, headers=headers)


async def request_hotels_info(ids: List[str], token: str, date_in: str, date_out: str, adults: int):
    url = 'https://test.api.amadeus.com/v3/shopping/hotel-offers'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'hotelIds': ','.join(ids),
        'checkInDate': date_in,
        'checkOutDate': date_out,
        'lang': 'RU',
        'roomQuantity': 1,
        'adults': adults,
    }

    return await client.get(url, params=params, headers=headers)


async def request_token():
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'grant_type': 'client_credentials',
        'client_id': AMADEUS_TOKEN,
        'client_secret': AMADEUS_SECRET,
    }
    response = await client.post(headers=headers, data=params, url=url)
    return response.json()['access_token']


async def get_hotels(lat: float, lon: float, date_in: str, date_out: str, adults: int) -> Tuple[str, List]:
    token = await request_token()
    response = await request_hotels_list(lat, lon, token)
    if response.status_code != 200 or not response.json():
        return Templates.OPENTRIP_ERROR.value, []
    ids = []
    for hotel in response.json()['data']:
        ids.append(hotel['hotelId'])

    response = await request_hotels_info(ids, token, date_in, date_out, adults)

    if 'data' not in response.json():
        return Templates.NO_HOTELS.value, []

    res = ''
    locs = []
    for index, element in enumerate(response.json()['data'], 1):
        if element['type'] != 'hotel-offers' or not element['available']:
            continue
        hotel = element['hotel']
        lat, lon = hotel['latitude'], hotel['longitude']
        name = hotel['name']
        offer = element['offers'][0]

        desc = offer['room']['description']['text']
        price = offer['price']

        if 'total' in price:
            cost = price['total']
        else:
            cost = price['base']
        locs.append((lat, lon))
        currency = price['currency']
        price_str = f'{cost} {currency}'
        res += TemplatesGen.hotel(name, desc, price_str, index)

    return res, locs
