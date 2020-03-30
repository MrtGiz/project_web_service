WEB SERVICE (test)
==================
Асинхронный веб-сервис, выполняющий обработку получаемых сообщений.
Включает в себя:
- Веб-сервис (получатель)
- Обработчик
- База данных - PostgreSQL
- RabbitMQ (для общения микросервисов между собой)

Инструкция по запуску
---------------------
Настройка среды разработки
__________________________

Клолнирование проекта:


    git clone https://github.com/MrtGiz/project_web_service.git
    cd aio-pika

Создание нового virtualenv:

    $ virtualenv -p python3.7 env

Установка необходимых зависимостей:

    $ pip install aiohttp


Запуск проекта
______________
В корневой папке проекта:

    $ docker-compose up
    
После запуска всех сервисов для тестирования приема POST запросов:

    $ python client.py
    
Мониторинг состояния БД и брокера сообщений
___________________________________________


Администрирование БД: http://localhost:8090/    (user/pass: postgres/qwerty123)

Мониторинг RabbitMQ: http://localhost:15672/    (user/pass: guest/guest)