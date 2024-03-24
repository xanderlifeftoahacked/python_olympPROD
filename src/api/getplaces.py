from os import getenv

from api.httpxclient import client
from templates.travel_helper import Templates

OPENTRIPMAP_TOKEN = '5ae2e3f221c38a28845f05b671e590faf71b9e5f639de9b84e1fe6b8'
if getenv('RUNNING_DOCKER'):
    GRAPHHOPPER_TOKEN = str(getenv('GRAPHHOPPER_TOKEN'))
    GEOAPIFY_TOKEN = str(getenv('GEOAPIFY_TOKEN'))
    OPENTRIPMAP_TOKEN = str(getenv('OPENTRIPMAP_TOKEN'))
OPENTRIPMAP_TOKEN = '5ae2e3f221c38a28845f05b671e590faf71b9e5f639de9b84e1fe6b8'


def get_url_interesting_places(lat: float, lon: float):
    return f'https://api.opentripmap.com/0.1/ru/places/radius?radius=10000&rate=3h&limit=20&kinds=interesting_places&lon={lon}&lat={lat}&apikey={OPENTRIPMAP_TOKEN}'


async def get_interesting_places(lat: float, lon: float) -> str:
    response = await client.get(get_url_interesting_places(lat, lon))
    if response.status_code != 200 or not response.json():
        return Templates.OPENTRIP_ERROR.value

    if not response.json()['features']:
        return Templates.NO_INTERESTING.value

    valid_places = []
    for place in response.json()['features']:
        if place['properties']['name']:
            valid_places.append(place)
    print(valid_places)
    return "HAHA"
