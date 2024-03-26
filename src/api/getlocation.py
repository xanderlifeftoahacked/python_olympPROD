from typing import Any, List, Tuple

from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='xander_traveltg',
                       adapter_factory=AioHTTPAdapter, timeout=5)  # noqa #type: ignore


async def get_coords_from_raw(loc: str) -> List[Any]:
    location = await geolocator.geocode(loc, language='ru')  # noqa #type: ignore
    if not location:
        return [None, None, None]
    return [location.latitude, location.longitude]  # noqa #type:ignore


async def get_location_from_raw(loc: str) -> Any:
    location = await geolocator.geocode(loc, language='ru')  # noqa #type:ignore

    if not location:
        return [None, None, None]
    return location.address, location.latitude, location.longitude


async def get_location(lat: float, lon: float) -> Any:
    location = await geolocator.reverse((lat, lon), language='ru')  # noqa #type:ignore

    if not location:
        return None
    return location.address


async def get_country_city(lat: float, lon: float) -> Tuple[Any, Any, Any]:
    location = await geolocator.reverse((lat, lon), language='ru')  # noqa #type:ignore

    if not location:
        return None, None, None

    if 'country' not in location.raw['address']:
        return None, None, None

    country = location.raw['address']['country']
    city = []
    if 'town' in location.raw['address']:
        city.append(location.raw['address']['town'])
    if 'county' in location.raw['address']:
        city.append(location.raw['address']['county'])
    if 'city' in location.raw['address']:
        city.append(location.raw['address']['city'])

    return country, ', '.join(city), (location.latitude, location.longitude)


async def get_country_city_from_raw(location_str: str) -> Tuple[Any, Any, Any]:
    location = await geolocator.geocode(location_str, addressdetails=True, language='ru')  # noqa #type:ignore

    if not location:
        return None, None, None

    if 'country' in location.raw['address']:
        country = location.raw['address']['country']
        city = location.raw['name']
        return country, city, (location.latitude, location.longitude)
    else:
        return None, None, None
