from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='xander_travelbot')


def get_country_city(lat, lon):
    location = geolocator.reverse((lat, lon), language='ru')  # noqa #type: ignore

    country = location.raw['address']['country']  # noqa #type: ignore
    city = location.raw['address']['city']  # noqa #type: ignore

    return country, city
