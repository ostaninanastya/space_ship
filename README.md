# Space ship

ITMO project

## Logbook

Основанный на clickhouse набор журналов, содержащих данные о работе гипотетического космического корабля

### Entities

* control_action - описывает команду, когда-либо выданную системе управления кораблем (например, повернуть налево или снять показания датчиков космического излучения по левому борту)
* position - описывет скорость и положение корабля в космосе в данный момент времени при помощи трех координат : x, y, z, угла между продольной осью корабля и осью OX (угол атаки), угла между проекцией продольной осью корабля на плоскость XOY и осью OX (угол направления)
* sensor_data - содержит показания приборов в данный момент времени (например, концентрация холодной темной материи у верхнего края корабля)
* system_state - предназначена для мониторинга состояния систем корабля

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, для которой актуально приведенное состояние системы|
|system name|text|Название системы, состояние которой было зафиксировано|
|system id|UUID|Идентификатор системы, состояние которой было зафиксировано|
|status|text|Состояние системы, может принимать значения **working, fail, being_fixed, testing**|

### Prerequisites

Требуются установленные:

#### clickhouse-server

Cобственно сервер, на котором будет лежать база данных

Установка производится так:

Прописать в  **/etc/apt/sources.list** репозиторий **deb http://repo.yandex.ru/clickhouse/deb/stable/ main/**

Выполнить команды

    sudo apt-get update
    sudo apt-get install clickhouse-client clickhouse-server-common

#### infi.clickhouse_orm

Модуль для python, с помощью которого идет взаимодействие с БД

Устанавливается командой

    pip install infi.clickhouse_orm
  
### Running

#### Server

Выполнить команду

    sudo clickhouse-server --config-file=/etc/clickhouse-server/config.xml
  
#### Client

Для выполнения SQL запросов в командной строке. Запускается командой

    clickhouse-client
  
#### Scripts

После запуска сервера необходимо сначала инициализировать базу данных соответствующими таблицами

    DB_URL=http://127.0.0.1:8123 DB_NAME=logbook python3 initialize.py
  
Проверить в клиенте что все таблицы созданы

    show tables from logbook
  
Заполнить базу данных значениями, если они были заранее сгенерированы

    DB_URL=http://127.0.0.1:8123 DB_NAME=logbook python3 fill.py
  
В противном случае сначла сгенерировать значения (следующая команда запускается из папки generators)
  
    python3 main.py
  
В скрипте можно изменять объем данных для генерации
  
Далее можно проверить что все прошло успешно запуском ряда простых манипуляций с данными

    DB_URL=http://127.0.0.1:8123 DB_NAME=logbook python3 explore.py
  
## Communications

### Entities

### Prerequisites

Требуются установленные:

#### neo4j server

Cобственно сервер, на котором будет лежать база данных

Установка производится так:

    wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
    echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list
    sudo apt update
    sudo apt install neo4j

#### neomodel

Модуль для python, с помощью которого идет взаимодействие с БД

Устанавливается командой

    pip install neomodel
  
### Running

#### Server

Выполнить команду

    sudo service neo4j start
  
#### Client

Для выполнения запросов в web интерфейсе и просмотра полученного графа. Запускается в браузере по адресу

    http://localhost:7474
  
#### Scripts

Тестовый скрипт создает классы смены, операции, человека и устанавливает базовые коммуникации между тем, формируя простейший граф

    USERNAME=neo4j PASSWORD=neo4j python3 test.py

  
