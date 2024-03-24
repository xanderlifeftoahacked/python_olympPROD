from asyncio import to_thread
from staticmap import IconMarker, Line, StaticMap
from math import ceil
from os import getenv
from typing import Any, List, Tuple
from polyline import decode

from api.httpxclient import client
from templates.travel_helper import Templates

GRAPHHOPPER_TOKEN = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
FLAG_ICON_BIG = './samples/flag_big.png'  # 64 x 64
FLAG_ICON_SMALL = './samples/flag_small.png'  # 32 x 32

graphhopper_url = 'https://graphhopper.com/api/1/'
if getenv('RUNNING_DOCKER'):
    GRAPHHOPPER_TOKEN = str(getenv('GRAPHHOPPER_TOKEN'))


def generate_graphhopper_url(locations: List[List[Any]]) -> str:
    points = '&point='.join([','.join([str(location[1]), str(location[2])])
                             for location in locations])

    return f'{graphhopper_url}route?point={points}&vehicle=car&key={GRAPHHOPPER_TOKEN}'


def generate_markers(locations: List[Any]) -> List[IconMarker]:
    markers = []
    for location in locations:
        marker = IconMarker(
            (location[0], location[1]), FLAG_ICON_BIG, 32, 52)
        markers.append(marker)
    return markers


def generate_markers_for_places(locations: List[Any], main_lat: float, main_lon: float) -> List[IconMarker]:
    markers = []
    for location in locations:
        marker = IconMarker(
            (location[1], location[0]), FLAG_ICON_SMALL, 16, 26)
        markers.append(marker)
    markers.append(IconMarker((main_lon, main_lat), FLAG_ICON_BIG, 32, 52))
    return markers


async def make_markers_map(locations: List[Tuple[float, float]], main_lat: float, main_lon: float) -> Any:
    try:
        m = StaticMap(1920, 1080)
        markers = generate_markers_for_places(
            locations, main_lat, main_lon)
        for marker in markers:
            m.add_marker(marker)
        img = await to_thread(m. render)
    except Exception:
        return False, Templates.OSM_ERROR.value, None

    return True, Templates.ROUTE_READY.value, img


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
    decoded_polyline = decode(encoded_polyline, geojson=True)

    shorted_polyline = []
    for i in range(0, len(decoded_polyline), ceil(len(decoded_polyline) / 300)):
        shorted_polyline.append(decoded_polyline[i])
    line = Line(shorted_polyline, '#4169E1', 8)

    try:
        map = StaticMap(1920, 1080)
        for location in locations:
            marker = IconMarker(
                location[2:0:-1], FLAG_ICON_BIG, 32, 52)
            map.add_marker(marker)

        map.add_line(line)
        img = await to_thread(map.render)

    except Exception:
        return False, Templates.OSM_ERROR.value, None

    return True, Templates.ROUTE_READY.value, img
