# TravelBot by xander (@travel_xanderbot)

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
### Регистрация
https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/f2f5ca33-5e36-4c83-b932-e8121a474f18

### Добавление путешествий
https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/2f28f3e6-4928-4551-8d8e-47819d4d954f

### Настройки путешествия
https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/48a3a889-72ac-4b04-8884-4e4bfcdd7893

### Управление заметками
https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/assets/61379005/fe2dd719-fb96-4c41-8b4a-0c9b3635ad3d



## Интеграции
### СУБД
В качестве СУБД была выбрана SQLite (для работы с ней используется асинхронный драйвер). Другим вариантом мог быть PostgreSQL, предлагающий больший функционал, однако функционала SQLite мне более чем достаточно. К тому же, SQLite выигрывает у Postgres в скорости.
От кэширования (например, с помощью Redis) я отказался по причине того, что выигрыш в скорости получения и записи данных был бы нивелирован временем ожидания ответов от API (даже самого Telegram).   
### Библиотеки
  * Aiogram - один из популярных фреймворков для работы с Telegram Bot Api. Был выбран исходя из рекомендаций сообщества.
  * SQLAlchemy - ORM для более удобной и безопасной работы с базой данных.
  * Aiosqlite - асинхронный драйвер для базы данных.
  * Dateparser - 
  * Pyowm - 
  * Geopy - 
  * Httpx - 
  * Polyline - 
  * Dateparser
  * Staticmap -
  * Pillow -
### Сторонние API


## Структура базы данных

<img src="https://github.com/Central-University-IT-prod/backend-xanderlifeftoahacked/blob/main/.readmemedia/database_schema.png" width="500"/>
