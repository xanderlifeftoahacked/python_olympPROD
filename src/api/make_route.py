import asyncio
import json
import io
from os import getenv
from typing import Any, List, Tuple
import requests
from polyline import decode
import folium
from PIL import Image
from api.getlocation import get_coords_from_raw
from templates.travel_helper import Templates

GRAPHHOPPER_TOKEN = str(getenv('GRAPHHOPPER_TOKEN'))
GRAPHHOPPER_TOKEN = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
GIST_TOKEN = str(getenv('GIST_TOKEN'))
GIST_TOKEN = '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'
graphhopper_url = 'https://graphhopper.com/api/1/'
gist_url = 'https://api.github.com/gists'
gist_headers = {
    'Authorization': f'token {GIST_TOKEN}'
}


def generate_gist_data_json(text: str) -> str:
    return json.dumps({
        'description': 'Gist for rendering map',
        'public': True,
        'files': {
            'map.html': {
                'content': text
            }
        }
    })


async def gist_post(data: str) -> requests.Response:
    return await asyncio.to_thread(requests.post, url=gist_url, headers=gist_headers,
                                   data=generate_gist_data_json(data))


async def try_to_build_route(locations: List[List[str]], from_raw=True) -> Tuple[bool, str, Any]:
    if from_raw:
        locations_with_coords = [[get_coords_from_raw(
            location[0]), location[1], location[2]] for location in locations]
        sorted_locations = sorted(locations_with_coords,
                                  key=lambda x: x[1])
    else:
        locations_with_coords = [[get_coords_from_raw(
            location[0]), None, None] for location in locations]
        sorted_locations = locations_with_coords

    points = '&point='.join([','.join([str(location[0][0]), str(location[0][1])])
                             for location in sorted_locations])
    get_route_url = f'{graphhopper_url}route?point={points}&vehicle=car&key={GRAPHHOPPER_TOKEN}'
    response = await asyncio.to_thread(requests.get, get_route_url)
    if response.status_code == 400:
        return False, Templates.NO_ROUTE.value, None

    if response.status_code != 200:
        return False, Templates.ROUTING_ERROR.value, None

    route_data = response.json()

    if 'paths' in route_data or not route_data['paths']:
        encoded_polyline = route_data['paths'][0]['points']
    else:
        return False, Templates.NO_ROUTE.value, None

    decoded_polyline = decode(encoded_polyline)  # noqa #type: ignore

    map_center = [float(sorted_locations[0][0][0]),
                  float(sorted_locations[0][0][1])]
    map_route = folium.Map(location=map_center, zoom_start=5)
    lats = [point[0] for point in decoded_polyline]
    lons = [point[1] for point in decoded_polyline]

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    map_route.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    folium.PolyLine(locations=decoded_polyline,
                    color='blue').add_to(map_route)

    img_data = map_route._to_png(1)
    img = Image.open(io.BytesIO(img_data))

    response = await gist_post(map_route.get_root().render())  # noqa #type: ignore

    if response.status_code != 201:
        return False, Templates.GIST_ERROR.value, None

    return True, response.json()['files']['map.html']['raw_url'].replace('githubusercontent', 'githack'), img
