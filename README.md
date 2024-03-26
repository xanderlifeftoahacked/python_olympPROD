# TravelBot by xander ([@travel_xanderbot](https://t.me/travel_xanderbot))


<a target="_blank" href="https://github.com/docker"><img src="https://img.shields.io/badge/Docker-blue"/></a> </a> 
<a target="_blank" href="https://github.com/aiogram"><img src="https://img.shields.io/badge/Aiogram-blue"/></a> </a> 
<a target="_blank" href="https://github.com/sqlite"><img src="https://img.shields.io/badge/SQLite-gray"/></a> </a> 
<a target="_blank" href="https://github.com/python"><img src="https://img.shields.io/badge/Python-yellow"/></a> </a> 

## Инструкция по запуску
Для запуска контейнера необходимы Docker, Docker-Compose и включенный docker.service. Пример запуска контейнера на arch-linux:
```
~ » sudo pacman -Sy docker docker-compose git
~ » git clone git@github.com:Central-University-IT-prod/backend-xanderlifeftoahacked.git
~ » sudo systemctl start docker
~ » cd backend-xanderlifeftoahacked
~/backend-xanderlifeftoahacked (main) » sudo docker-compose up --build
```
Пример запуска вне контейнера:
```
~ » sudo pacman -Sy python python-virtualenv git
~ » git clone git@github.com:Central-University-IT-prod/backend-xanderlifeftoahacked.git
~ » cd backend-xanderlifeftoahacked
~/backend-xanderlifeftoahacked (main) » python -m venv venv
~/backend-xanderlifeftoahacked (main) » source venv/bin/activate
~/backend-xanderlifeftoahacked (main) (venv) » pip install -r requirements.txt --upgrade pip
~/backend-xanderlifeftoahacked (main) (venv) » export BOT_TOKEN=...  // скопировать переменные окружения из docker-compose.yml
~/backend-xanderlifeftoahacked (main) (venv) » python src/bot.py
```

## Функционал бота
**_На момент заверешения работы над ботом его функционал, вид кнопок и т.п. могут незначительно отличаться от представленных на видео и скриншотах._**
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
На данный момент межконтинентальные маршруты невозможны

_upd: В поздних версиях появился выбор между источниками статических карт (быстрый, но проприетарный/помедленнее, но  open-source)_

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/5e0c2ac4-50b1-479f-942c-7b3453be69f6

### Просмотр отелей
Второй пункт меню помощника. Покажет ближашие номера (название отеля, описание, цена) доступные на даты посещения места. 
Также отправит карту, на которой будут отмечены отели. 

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/c075fc76-d174-4604-a1fc-66ccc8b42568


### Просмотр погоды
Третий пункт меню помощника. Покажет прогноз погоды на даты посещения локации (но только на те, что не позже 16 дней от текущей) . 
Прогноз содержит температуру, местное время восхода и захода солнца и осадки. 

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/982f009c-9649-4a74-a51f-309464284c3a

### Просмотр кафе и ресторанов
Четвертый пункт меню помощника. Вернет список кафе и ресторанов с названиями, адресами, временем работы и ссылками на их сайты (если таковые присутствуют).
Отправит соответствующую карту.

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/01f00e07-1318-48fc-89f6-6277d11b7216


### Просмотр достопримечательностей
Пятый пункт меню помощника. Отправит десять самых популярных достопримечательностей (название, адрес, описание) в радиусе 10 километров от выбранной локации. Также отправит карту, 
на которой эти достопримечательности будут отмечены.

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/f93be38b-e5cf-4797-b178-a42e1908cea6

### Переводчик
В путешествии очень удобно иметь возможность быстро записать чей-то голос и увидеть его перевод. Так же есть обратная возможность - наговорить текст на русском 
и получить перевод на русский язык.

https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/b66a893f-76d1-4897-ac7d-1428e8b9d42e



## Интеграции
### СУБД
В качестве СУБД была выбрана SQLite (для работы с ней используется асинхронный драйвер). Другим вариантом мог быть PostgreSQL, предлагающий больший функционал, однако функционала SQLite мне более чем достаточно.
От кэширования (например, с помощью Redis) я отказался по причине того, что выигрыш в скорости получения и записи данных был бы нивелирован временем ожидания ответов от API (даже самого Telegram).   
### Библиотеки (многие из них очень маленькие, в несколько классов (прослойки для взаимодействия с API))
  * **Aiogram** - один из популярных фреймворков для работы с Telegram Bot Api. Был выбран исходя из рекомендаций сообщества.
  * **SQLAlchemy** - ORM для более удобной и безопасной работы с базой данных.
  * **Aiosqlite** - асинхронный драйвер для базы данных.
  * **Open-meteo** - получение информации о погоде (билиотека находится в директории src/lib, я внес в нее одно небольшое изменение)
  * **Geopy** - геокодинг (поиск локаций)
  * **Httpx** - асинхронные url-запросы
  * **Polyline** - используется для декодирования маршрутов, полученных от API
  * **Dateparser** - используется для распознования дат
  * **Pillow** - используется для работы с изображениями
  * **Staticmap** - испольуется для получения изображений карты
  * **TimezonefinderL** - используется для получения часового пояса из координат
  * **AssemblyAI** - используется для извлечения текста из голосовых сообщений
  * **Translate** - используется для перевода текста
### Сторонние API
#### OSM-based (используют OSM):
  * **Nominatim** ([repo](https://github.com/osm-search/Nominatim)) - используется для геокодинга (через geopy)
  * **Graphhopper** ([repo](https://github.com/graphhopper/graphhopper)) - используется для построения маршрутов
  * **OSM carto** ([repo](https://github.com/gravitystorm/openstreetmap-carto/)) - используется для получения изображений с маршрутом (через библиотеку staticmap)
#### Остальные:
  * **Open-meteo** ([repo](https://github.com/frenck/python-open-meteo)) - используется для получения данных о погоде (через одноименную библиотеку)
  * **Foursquare** ([page](https://location.foursquare.com/)) - используется для получения данных о достопримечательностях и кафе (разрешено около 40 тыс. бесплатных запросов в месяц)
  * **Static API yandex** ([page](https://yandex.ru/maps-api/products/static-api)) - используется как альтернативный способ получения изображения маршрута, очень быстрое (используется тариф 'бесплатный')
  * **Amadeus** ([page](https://developers.amadeus.com/)) - единственное API для поиска отелей, которым возможно пользоваться бесплатно (из тех, что я находил). База отелей очень маленькая, информации о каждом
    отдельном номере/отеле тоже очень мало. Работает долго. Однако ничего более сносного не нашлось.
  * **Yandex поиск организаций** ([page](https://yandex.ru/maps-api/products/geosearch-api)) - API для поиска кафе и ресторанов. Очень быстрое, информации достаточно (использутся тариф 'пробный')
  * **AssemblyAI** ([page](https://www.assemblyai.com/)) - используется для извлечения текста из голосовых сообщений (через одноименную библиотеку)
  * **MyMemory** ([repo](https://github.com/UlionTse/translators)) - используется библиотекой translate для перевода
      
 
## Структура базы данных

<img src="https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/blob/main/.readmemedia/database_schema.png" width="500"/>
