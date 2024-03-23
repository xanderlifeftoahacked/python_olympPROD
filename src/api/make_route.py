from PIL import Image
from math import ceil
from polyline.polyline import io
from os import getenv
from typing import Any, List, Tuple
from polyline import decode

from api.httpxclient import client
from templates.travel_helper import Templates

GRAPHHOPPER_TOKEN = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
GEOAPIFY_TOKEN = 'c5429f227e67422fa582ad93623882c1'
graphhopper_url = 'https://graphhopper.com/api/1/'

if getenv('RUNNING_DOCKER'):
    GRAPHHOPPER_TOKEN = str(getenv('GRAPHHOPPER_TOKEN'))
    GEOAPIFY_TOKEN = str(getenv('GEOAPIFY_TOKEN'))

marker_params = ';type:awesome;iconsize:large;color:%23144a10;size:large;shadow:no;icontype:awesome;icon:flag|'


def generate_geoapify_url(decoded_polyline: List[Tuple[float, float]], markers_string: str) -> str:
    shorted_polyline = []
    for i in range(0, len(decoded_polyline), ceil(len(decoded_polyline)/300)):
        shorted_polyline.append(decoded_polyline[i])
    polyline_string = ','.join(
        [f"{lat},{lon}" for lon, lat in shorted_polyline])

    return (f'https://maps.geoapify.com/v1/staticmap?'
            f'width=1920&height=1080&'
            f'apiKey={GEOAPIFY_TOKEN}&'
            f'geometry=polyline:{polyline_string};linewidth:8;linecolor:%23144a10&'
            f'{markers_string}')


def generate_graphhopper_url(locations: List[List[Any]]) -> str:
    points = '&point='.join([','.join([str(location[1]), str(location[2])])
                             for location in locations])

    return f'{graphhopper_url}route?point={points}&vehicle=car&key={GRAPHHOPPER_TOKEN}'


def generate_markers_str(locations: List[Any]) -> str:
    markers_str = "marker="
    marker_params = 'type:awesome;iconsize:large;color:%23144a10;size:large;shadow:no;icontype:awesome;icon:flag'
    for location in locations:
        marker = f"lonlat:{','.join([str(x) for x in location[2:0:-1]])};{marker_params}|"
        markers_str += marker
    return markers_str[:-1]


async def try_to_build_route(locations: List[List[Any]], from_raw=True) -> Tuple[bool, str, Any]:
    if from_raw:
        locations = sorted(locations,
                           key=lambda x: x[3])

    response = await client.get(generate_graphhopper_url(locations))

    if response.status_code == 400:
        return False, Templates.NO_ROUTE.value, None

    if response.status_code != 200:
        return False, Templates.ROUTING_ERROR.value, None

    route_data = response.json()

    if 'paths' in route_data or not route_data['paths']:
        encoded_polyline = route_data['paths'][0]['points']
    else:
        return False, Templates.NO_ROUTE.value, None

    decoded_polyline = decode(encoded_polyline)

    url = generate_geoapify_url(
        decoded_polyline, generate_markers_str(locations))

    response = await client.get(url)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        return True, Templates.ROUTE_READY.value, img
    else:
        return False, Templates.OSM_ERROR.value, None
