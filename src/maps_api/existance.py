from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='xander_travelbot')

#


def check_country_existance(country_name):
    location = geolocator.geocode(
        country_name, language='ru', exactly_one=True)
    if not location or location.raw['addresstype'] != 'country':
        return None
    return location.raw['display_name']
#


def check_city_existance(country_name, city_name):
    location = geolocator.geocode(
        f'{country_name} {city_name}', language='ru', exactly_one=True)
    print(location.raw)
    if not location or (location.raw['addresstype'] != 'state' and location.raw['addresstype'] != 'city' and location.raw['addresstype'] != 'town'):
        return None
    return location.raw['display_name']
