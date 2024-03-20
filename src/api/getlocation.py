from typing import Any, List, Tuple
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='xander_travelbot')


def get_coords_from_raw(loc: str) -> List[float]:
    location = geolocator.geocode(loc, language='ru')  # noqa #type: ignore
    return [location.latitude, location.longitude]  # noqa #type: ignore


def get_location_from_raw(loc: str) -> Any:
    location = geolocator.geocode(loc, language='ru')  # noqa #type: ignore

    if not location:
        return None
    return location.address  # noqa #type: ignore


def get_location(lat: float, lon: float) -> Any:
    location = geolocator.reverse((lat, lon), language='ru')  # noqa #type: ignore

    if not location:
        return None
    return location.address  # noqa #type: ignore


def get_country_city(lat: float, lon: float) -> Tuple[Any, Any, Any]:
    location = geolocator.reverse((lat, lon), language='ru')  # noqa #type: ignore
    if not location:
        return None, None, None

    if 'country' not in location.raw['address']:  # noqa #type: ignore
        return None, None, None

    country = location.raw['address']['country']  # noqa #type: ignore
    city = []
    if 'town' in location.raw['address']:  # noqa #type: ignore
        city.append(location.raw['address']['town'])  # noqa #type: ignore
    if 'county' in location.raw['address']:  # noqa #type: ignore
        city.append(location.raw['address']['county'])  # noqa #type: ignore
    if 'city' in location.raw['address']:  # noqa #type: ignore
        city.append(location.raw['address']['city'])  # noqa #type: ignore

    return country, ', '.join(city), (location.raw['lat'] + ' ' + location.raw['lon'])  # noqa #type: ignore


def get_country_city_from_raw(location_str: str) -> Tuple[Any, Any, Any]:
    location = geolocator.geocode(
            location_str, addressdetails=True, language='ru')  # noqa #type: ignore

    if not location:
        return None, None, None

    if 'country' in location.raw['address']:  # noqa #type: ignore
        country = location.raw['address']['country']  # noqa #type: ignore
        city = location.raw['name']  # noqa #type: ignore
        return country, city, (location.raw['lat'] + ' ' + location.raw['lon'])  # noqa #type: ignore

    else:
        return None, None, None
