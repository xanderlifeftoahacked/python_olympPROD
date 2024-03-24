from os import getenv
from typing import List, Tuple

from api.httpxclient import client
from templates.travel_helper import Templates, TemplatesGen

if getenv('RUNNING_DOCKER'):
    FORSQUARE_TOKEN = str(getenv('AMADEUS_TOKEN'))

AMADEUS_TOKEN = 'NtqTBIoB2WebG58PviubAiyfR2sZYwZV'
headers = {
    'Authorization': f'Bearer {AMADEUS_TOKEN}'
}


async def request_hotels(lat: float, lon: float, date_in: str, date_out: str, adults: int):
    params = {
        'latitude': lat,
        'longitude': lon,
        'radius': 2,
        # 'checkInDate': date_in,
        # 'checkOutDate': date_out,
        # 'adults': adults
    }

    return await client.get(
        'https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode', params=params, headers=headers)


async def get_hotels(lat: float, lon: float, date_in: str, date_out: str, adults: int) -> Tuple[str, List]:
    response = await request_hotels(lat, lon, date_in, date_out, adults)
    print(response.json())
    # if response.status_code != 200 or not response.json():
    #     return Templates.OPENTRIP_ERROR.value, []
    #
    # response = response.json()
    # if not response['results']:
    #     return Templates.NO_INTERESTING.value, []
    # ans = ''
    # places = []
    # for place in response['results']:
    #     if 'description' in place:
    #         description = place['description']
    #     else:
    #         description = ''
    #     ans += TemplatesGen.place(is_open=place['hours']['open_now'],
    #                               name=place['name'],
    #                               description=description,
    #                               address=place['location']['formatted_address'],
    #                               distance=place['distance'])
    #     places.append((place['geocodes']['main']['latitude'],
    #                    place['geocodes']['main']['longitude']))
    return '', []
