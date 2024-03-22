from staticmap import CircleMarker, Line, StaticMap
import asyncio
from os import getenv
from typing import Any, List, Tuple
from polyline import decode
from api.httpxclient import client

from templates.travel_helper import Templates

GRAPHHOPPER_TOKEN = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
graphhopper_url = 'https://graphhopper.com/api/1/'

if getenv('RUNNING_DOCKER'):
    GRAPHHOPPER_TOKEN = str(getenv('GRAPHHOPPER_TOKEN'))


async def try_to_build_route(locations: List[List[Any]], from_raw=True) -> Tuple[bool, str, Any]:
    if from_raw:
        locations = sorted(locations,
                           key=lambda x: x[3])

    points = '&point='.join([','.join([str(location[1]), str(location[2])])
                             for location in locations])
    get_route_url = f'{graphhopper_url}route?point={points}&vehicle=car&key={GRAPHHOPPER_TOKEN}'
    response = await client.get(get_route_url)
    if response.status_code == 400:
        return False, Templates.NO_ROUTE.value, None

    if response.status_code != 200:
        return False, Templates.ROUTING_ERROR.value, None

    route_data = response.json()

    if 'paths' in route_data or not route_data['paths']:
        encoded_polyline = route_data['paths'][0]['points']
    else:
        return False, Templates.NO_ROUTE.value, None

    decoded_polyline = decode(encoded_polyline, geojson=True)  # noqa #type: ignore

    line = Line(decoded_polyline, 'blue', 8)

    try:
        map = StaticMap(1920, 1080)
        for location in locations:
            marker = CircleMarker(location[2:0:-1], 'orange', 30)
            map.add_marker(marker)

        map.add_line(line)
        img_data = await asyncio.to_thread(map.render)
        img = img_data

    except Exception:
        return False, Templates.OSM_ERROR.value, None

    return True, Templates.ROUTE_READY.value, img
