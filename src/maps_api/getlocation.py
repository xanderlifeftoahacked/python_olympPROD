from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='xander_travelbot')


def get_country_city(lat, lon):
    location = geolocator.reverse((lat, lon), language='ru')

    country = location.raw['address']['country']
    city = location.raw['address']['city']

    return country, city
