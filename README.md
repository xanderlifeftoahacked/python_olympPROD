# TravelBot by xander ([@travel_xanderbot](https://t.me/travel_xanderbot))

<a target="_blank" href="https://github.com/docker"><img src="https://img.shields.io/badge/Docker-blue"/></a> </a> 
<a target="_blank" href="https://github.com/aiogram"><img src="https://img.shields.io/badge/Aiogram-blue"/></a> </a> 
<a target="_blank" href="https://github.com/sqlite"><img src="https://img.shields.io/badge/SQLite-gray"/></a> </a> 
<a target="_blank" href="https://github.com/python"><img src="https://img.shields.io/badge/Python-yellow"/></a> </a> 

## Инструкция по запуску
Для запуска контейнера необходимы Docker, Docker-Compose и включенный docker.service. Пример запуска контейнера на arch-linux:
```
~ » git clone git@github.com:Central-University-IT-prod/backend-xanderlifeftoahacked.git
~ » sudo pacman -Sy docker docker-compose
~ » sudo systemctl start docker
~ » cd backend-xanderlifeftoahacked
~/backend-xanderlifeftoahacked (main) » sudo docker-compose up --build
```

## Функционал бота
**_! На момент заверешения работы над ботом его функционал, вид кнопок и т.п. могут незначительно отличаться от представленных на видео и скриншотах. !_**
### Регистрация
При регистрации пользователь поочередно вводит все необоходимые данные. С телефона можно поделиться местоположением для определения города.
С компьютера - написать текстом. Существует ограничение на максимальную длину описания. После регистрации можно изменить любые данные 
из своего профиля (кнопка 'Мой профиль' доступна из главного меню).

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/f2f5ca33-5e36-4c83-b932-e8121a474f18

### Добавление путешествий
Доступно из меню путешествий (кнопка 'Мои путешествия' главного меню). Пользователь вводит название и описание (на их длинну существуют ограничения),
затем начинается ввод локаций в формате 
Отправьте место -> Подтвердите -> Отправьте дату начала посещения -> Подтвердите -> Отправьте дату конца посещения -> Подтвердите.
После последнего подтверждения локация добавится в список. Можно отправить следующее место или завершить ввод.
Бот разрешает отправлять даты, начиная с текущей. Дата завершения не может быть раньше даты начала. После добавления путешествия, оно появляется в списке. 

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/2f28f3e6-4928-4551-8d8e-47819d4d954f

### Настройки путешествия
Кнопка настроек появляется под путешествиями при нажатии кнопки 'Просмотреть путешествия'. Из меню настроек можно изменять название и описание, 
добавлять и удалять локации и друзей. Доступно удаление путешествия (при нажатии бот переспросит о желании удалить путешествие).
Настройки и удаление путешествия доступны только его создателю (у друзей просто нет соотвествующих кнопок).

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/48a3a889-72ac-4b04-8884-4e4bfcdd7893

### Управление заметками
К путешествию можно добавлять файлы и изображения. Удалить заметку может только ее владелец, остальным доступен только просмотр (если заметка публичная)

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/fe2dd719-fb96-4c41-8b4a-0c9b3635ad3d

### Построение маршрутов
Первый пункт меню помощника. Можно построить маршрут от своего местоположения до первой точки путешествия. Либо маршрут через все точки 
путешествия. Результат пользователь получает в виде фотографии. Очередность локаций в маршруте определяется датами их посещения.

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/5e0c2ac4-50b1-479f-942c-7b3453be69f6

### Просмотр погоды
Третий пункт меню помощника. Покажет прогноз погоды на даты посещения локации (но только на те, что не позже 16 дней от текущей) . 
Прогноз содержит температуру, местное время восхода и захода солнца и осадки. 

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/982f009c-9649-4a74-a51f-309464284c3a




## Интеграции
### СУБД
В качестве СУБД была выбрана SQLite (для работы с ней используется асинхронный драйвер). Другим вариантом мог быть PostgreSQL, предлагающий больший функционал, однако функционала SQLite мне более чем достаточно. К тому же, SQLite выигрывает у Postgres в скорости.
От кэширования (например, с помощью Redis) я отказался по причине того, что выигрыш в скорости получения и записи данных был бы нивелирован временем ожидания ответов от API (даже самого Telegram).   
### Библиотеки
  * **Aiogram** - один из популярных фреймворков для работы с Telegram Bot Api. Был выбран исходя из рекомендаций сообщества.
  * **SQLAlchemy** - ORM для более удобной и безопасной работы с базой данных.
  * **Aiosqlite** - асинхронный драйвер для базы данных.
  * **Open-meteo** - получение информации о погоде (билиотека находится в директории src/lib, я внес в нее одно небольшое изменение)
  * **Geopy** - геокодинг (поиск локаций)
  * **Httpx** - асинхронные url-запросы
  * **Polyline** - используется для декодирования маршрутов, полученных от API
  * **Dateparser** - используется для распознования дат
  * **Pillow** - используется для работы с изображениями
  * **TimezonefinderL** - используется для получения часового пояса из координат
### Сторонние API
#### OSM-based (используют OSM):
  * **Nominatim** ([repo](https://github.com/osm-search/Nominatim)) - используется для геокодинга (через geopy)
  * **Graphhopper** ([repo](https://github.com/graphhopper/graphhopper)) - используется для построения маршрутов
  * **Geoapify (static map api)** ([osm wiki](https://wiki.openstreetmap.org/wiki/Geoapify)) - используется для получения изображений с маршрутом
  * **OpenTripMap** ([rapidapi](https://rapidapi.com/opentripmap/api/places1/details)) - используется для поиска достопримечательностей и кафе
#### Остальные:
  * **Open-meteo** ([repo](https://github.com/frenck/python-open-meteo)) - используется для получения данных о погоде (через одноименную библиотеку)

## Структура базы данных

<img src="https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/blob/main/.readmemedia/database_schema.png" width="500"/>
