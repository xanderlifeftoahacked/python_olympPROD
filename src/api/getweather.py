from datetime import datetime

from timezonefinderL import TimezoneFinder

from lib.openmeteo import DailyParameters, OpenMeteo
from templates.travel_helper import Templates, TemplatesGen

weather_mapping = {
    0: "Ясно",
    1: "Облачно",
    2: "Облачно",
    3: "Облачно",
    45: "Туман",
    48: "Сильный туман",
    51: "Изморось",
    52: "Изморось",
    53: "Изморось",
    55: "Изморось",
    56: "Ледяной дождик",
    57: "Ледяной дождик",
    61: "Ледяной дождик",
    63: "Дождь",
    65: "Сильный дождь",
    66: "Ледяной дождь",
    67: "Сильный ледяной дождь",
    71: "Снежок",
    73: "Снег",
    75: "Снегопад",
    77: "Снежный град",
    80: "Ливень",
    81: "Ливень",
    82: "Сильный ливень",
    85: "Снегопад",
    86: "Сильный снегопад",
    95: "Гроза",
    96: "Сильная гроза",
    99: "Сильная гроза"
}


tzw = TimezoneFinder()


def get_time_zone(lat: float, lon: float):
    tz = tzw.timezone_at(lat=lat, lng=lon)
    if tz:
        return tz
    else:
        return 'Etc/GMT'


def decode_weathercode(code: int) -> str:
    if code in weather_mapping:
        return weather_mapping[code]
    else:
        return ''


def get_datetime(date) -> datetime:
    return datetime(year=date.year, month=date.month, day=date.day)


async def get_weather(lat: float, lon: float, date_in: datetime, date_out: datetime) -> str:
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=lat,
            longitude=lon,
            current_weather=True,
            daily=[DailyParameters.TEMPERATURE_2M_MAX,
                   DailyParameters.TEMPERATURE_2M_MIN,
                   DailyParameters.SUNRISE,
                   DailyParameters.SUNSET,
                   DailyParameters.WEATHER_CODE],
            timezone=get_time_zone(lat, lon),
            forecast_days=16
        )

        if not forecast or not forecast.daily:
            return Templates.NO_WEATHER.value

        ans = ''
        for i in range(16):
            if date_in > get_datetime(forecast.daily.time[i]) or date_out < get_datetime(forecast.daily.time[i]):
                continue

            sunrise = forecast.daily.sunrise[i]  # noqa #type: ignore
            sunset = forecast.daily.sunset[i]  # noqa #type: ignore
            temp_min = forecast.daily.temperature_2m_min[i]  # noqa #type: ignore
            temp_max = forecast.daily.temperature_2m_max[i]  # noqa #type: ignore
            weather_code = forecast.daily.weathercode[i]  # noqa #type: ignore
            date = forecast.daily.time[i]  # noqa #type: ignore
            day_forecast_str = TemplatesGen.weather(sunrise, sunset, temp_min,
                                                    temp_max, decode_weathercode(weather_code), get_datetime(date))
            if ans == '':
                ans += f' {day_forecast_str}\n'
            else:
                ans += f'    {day_forecast_str}\n'

        if not ans:
            return f' {Templates.DONT_KNOW.value}\n'

        return ans

# if __name__ == '__main__':
#     asyncio.run(get_weather(55.715406, 37.438976, datetime.now()))
