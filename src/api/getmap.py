import io
from asyncio import to_thread
from math import ceil
from os import getenv
from typing import Any, List, Tuple

from PIL import Image
from polyline import decode
from staticmap import IconMarker, Line, StaticMap

from api.httpxclient import client
from templates.travel_helper import Templates

FLAG_ICON_BIG = './samples/flag_big.png'  # 64 x 64
FLAG_ICON_SMALL = './samples/flag_small.png'  # 32 x 32
graphhopper_url = 'https://graphhopper.com/api/1/'

YANDEX_TILES_TOKEN = str(getenv('YANDEX_TILES_TOKEN'))
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


async def make_markers_map(locations: List[Tuple[float, float]], main_lat: float, main_lon: float) -> Any:
    markers = ''.join([f'{y},{x},pmwtm{index}~' for index,
                      (x, y) in enumerate(locations, 1)])
    markers += f'{main_lon},{main_lat},pm2rdl'
    url = ('https://static-maps.yandex.ru/v1?'
           f'pt={markers}&size=640,450&'
           f'apikey={YANDEX_TILES_TOKEN}')

    response = await client.get(url)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        return True, Templates.ROUTE_READY.value, img
    else:
        return False, Templates.OSM_ERROR.value, None


async def get_polyline(locations: List[List[Any]]) -> List[Tuple[float, float]]:
    response = await client.get(generate_graphhopper_url(locations))

    if response.status_code == 400:
        raise RuntimeError(Templates.NO_ROUTE.value)

    if response.status_code != 200:
        raise RuntimeError(Templates.ROUTING_ERROR.value)

    route_data = response.json()

    if 'paths' in route_data or not route_data['paths']:
        encoded_polyline = route_data['paths'][0]['points']
    else:
        raise RuntimeError(Templates.NO_ROUTE.value)

    return decode(encoded_polyline, geojson=True)


async def get_route_image(locations: List[List[Any]], from_raw=True, yandex=True) -> Tuple[bool, str, Any]:
    if from_raw:
        locations = sorted(locations,
                           key=lambda x: x[3])
    try:
        decoded_polyline = await get_polyline(locations)
    except RuntimeError as e:
        return False, str(e), None

    shorted_polyline = []
    for i in range(0, len(decoded_polyline), ceil(len(decoded_polyline) / 100)):
        shorted_polyline.append(decoded_polyline[i])
    locs = [x[2:0:-1] for x in locations]

    if yandex:
        return await get_route_image_yandex(shorted_polyline, locs)
    else:
        return await get_route_image_osm(shorted_polyline, locs)


async def get_route_image_yandex(polyline: List[Tuple[float, float]], locs: List[Any]):
    vericies = ','.join([f'{x},{y}' for x, y in polyline])
    markers = ''.join([f'{x},{y},pm2orgm~' for x, y in locs])
    url = ('https://static-maps.yandex.ru/v1?'
           f'pl=c:8822DDC0,w:4,{vericies}&'
           f'pt={markers[:-1]}&size=650,450&'
           f'apikey={YANDEX_TILES_TOKEN}')

    response = await client.get(url)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        return True, Templates.ROUTE_READY.value, img
    else:
        return False, Templates.OSM_ERROR.value, None


async def get_route_image_osm(polyline: List[Tuple[float, float]], locs: List[Any]):
    try:
        map = StaticMap(1280, 720, 10, 10, headers={
                        'User-Agent': 'Travelbot'})
        for location in locs:
            marker = IconMarker(
                location, FLAG_ICON_BIG, 32, 52)
            map.add_marker(marker)

        line = Line(polyline, '#4169E1', 8)
        map.add_line(line)
        img = await to_thread(map.render)

    except Exception:
        return False, Templates.OSM_ERROR.value, None

    return True, Templates.ROUTE_READY.value, img
