from os import getenv
from typing import List, Tuple

from api.httpxclient import client
from templates.travel_helper import Templates, TemplatesGen

if getenv('RUNNING_DOCKER'):
    FORSQUARE_TOKEN = str(getenv('FORSQUARE_TOKEN'))

FORSQUARE_TOKEN = 'fsq3n82dG/o43vPRF1tApjgx2Z2wqeVjAzmYRO6KFEG7VZc='
headers = {
    'accept': 'application/json',
    'Accept-Language': 'ru',
    'Authorization': FORSQUARE_TOKEN
}


def get_url_interesting_places(lat: float, lon: float):
    return ('https://api.foursquare.com/v3/places/search?'
            f'll={lat},{lon}&radius=10000&categories=16000%2C10000&'
            'fields=name%2Clocation%2Cdistance%2Cdescription%2Chours%2Cgeocodes&'
            'sort=POPULARITY&limit=10')


async def get_interesting_places(lat: float, lon: float) -> Tuple[str, List]:
    response = await client.get(url=get_url_interesting_places(lat, lon), headers=headers)
    if response.status_code != 200 or not response.json():
        return Templates.OPENTRIP_ERROR.value, []

    response = response.json()
    if not response['results']:
        return Templates.NO_INTERESTING.value, []
    ans = ''
    places = []
    for place in response['results']:
        if 'description' in place:
            description = place['description']
        else:
            description = ''
        ans += TemplatesGen.place(is_open=place['hours']['open_now'],
                                  name=place['name'],
                                  description=description,
                                  address=place['location']['formatted_address'],
                                  distance=place['distance'])
        places.append((place['geocodes']['main']['latitude'],
                       place['geocodes']['main']['longitude']))
    return ans, places
