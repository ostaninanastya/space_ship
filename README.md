# Space ship

ITMO project

## Logbook

Основанный на cassandra db набор журналов, содержащих данные о работе гипотетического космического корабля

### Entities

* system_test - предназначена для записи результатов тестирования систем корабля

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, для которой актуально приведенное состояние системы|
|system id|12 bytes|Идентификатор системы, состояние которой было зафиксировано|
|result|int|Результат теста, может принимать значения от 0 до 100|

* control_action - описывает команду, когда-либо выданную системе управления кораблем (например, повернуть налево или снять показания датчиков космического излучения по левому борту)

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, определяющая момент получения команды|
|mac_address|6 bytes|MAC-адрес устройства, выдавшего команду|
|user_id|12 bytes|Идентификатор пользователя, выдавшего команду|
|command|text|Выданная команда (например, **get**)|
|params|text|Параметры, уточняющие, к какому результату должна привести команда (например, **--sensor=MINAS_MORGUL T400 --value_name=cold_dark_matter_concentration**)|
|result|text|Результат работы команды (например, **23.235715395881783 TeV**)|

* position - содержит историю перемещения корабля в космическом пространстве

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, определяющая момент получения команды|
|x|double|Координата корабля по оси OX, которая направлена от Земли в сторону планет не-Марс|
|y|double|Координата корабля по оси OY, которая перпендикулярна оси OX и направлена в сторону созвездия Кассиопея|
|z|double|Координата корабля по оси OZ|
|speed|double|Линейная скорость корабля|
|attack_angle|double|Угол между продольной осью корабля и осью OX|
|direction_angle|double|Угол между проекцией продольной осью корабля на плоскость XOY и осью OX|

* sensors_data - содержит данные о состоянии внешней среды, поставляемые сенсорами, расположенными по периметру корабля

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, определяющая момент получения данных от сенсора|
|source_id|12 bytes|Идентификатор сенсора, предоставившего данные|
|event|text|Наименование события, ставшего причиной фиксирования данных (например, **request**)|
|value_name|text|Название измеренной величины (например, **space_radiation**)|
|value|double|Значение измеренной величины|
|units|text|Единицы измерения (например, **eV** - сокрашение от электрон-вольт|

* shift_state - хранит обстановку в области, доверенной некоторой смене, на данный момент времени

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, для которой характерны данные о смене|
|shift_id|16 bytes|Идентификатор смены, для которой характерно зафикисированное состояние на некоторый момент времени|
|warning_level|text|Уровень опасности в районе, доверенном смене (может принимать значения **lowest**, **low**, **medium**, **heigh**, **highest**)|
|remaining_cartridges|double|Оставшиеся патроны (в процентах)|
|remaining_air|double|Оставшийся воздух (в процентах)|
|remaining_electricity|double|Оставшееся электричество (в процентах)|
|comment|text|Необязательный комментарий от работников смены|

* operation_state - содержит описание состояния операции на некоторый момент времени

|property|data type|description|
|--------|---------|-----------|
|time|timestamp|Временная отметка, для которой характерны данные об операции|
|boat_id|12 bytes|Необязательный идентификатор машины, зарезервированной для выполнения операции|
|operation_id|16 bytes|Идентификатор операции|
|operation_status|text|Состояние операции на данный момент времени (например, **detaching_from_ship**)|
|distance_to_the_ship|double|Расстояние от судна, предназначенного для операции, до корабля|
|zenith|double|Зенитный угол, задающий положение судна, предназначенного для операции, относительно корабля|
|azimuth|double|Азимутальный угол, задающий положение судна, предназначенного для операции, относительно корабля|
|hydrogenium|double|Процентное содержание водорода в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|helium|double|Процентное содержание гелия в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|...|double|115 полей, содержащих данные о процентном содержании химических элементов в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|oganesson|double|Процентное содержание оганесона в атмосфере / космической пыли вокруг команды, выполняющей операцию|
|comment|double|Необязательный комментарий от участников команды, выполняющей операцию|

### Prerequisites

Требуются установленные:

#### cassandra server

Для установки из debian packages (**изменить версию с 311x на актуальную**)

    echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
    curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
    sudo apt-get update
    sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
    sudo apt-get install cassandra

#### cassandra-driver

Модуль для python, с помощью которого идет взаимодействие с БД

Устанавливается командой (может занять несколько минут)

    pip install cassandra-driver

### pymongo

Модуль для python, с помощью которого идет взаимодействие с базой данных, содержащей информацию о корабле (работающей на технологии Mongo DB) для обеспечения консистентности хранимых данных при их изменении

Устанавливается командой 
    
    pip install pymongo

### py2neo

Модуль для python, с помощью которого идет взаимодействие с базой данных, содержащей информацию об организации деятельности экипажа (работающей на технологии neo4j) для обеспечения консистентности хранимых данных при их изменении

Устанавливается командой 

    pip install py2neo

### Running

#### Server

Выполнить команду, которая должна завершиться выводом информации о сервере с зеленым словом 'active'

    sudo service cassandra status

Для проверки статуса кластера выполнить

    sudo nodetool status

Должна вывести результат, начинающийся с сочетания **UN** (Up and Normal) в случае успеха
  
#### Client

Для выполнения SQL запросов в командной строке. Запускается командой

    cqlsh
  
#### Scripts

После запуска сервера необходимо сначала инициализировать базу данных соответствующими таблицами (параметры для подключения к базе данных автоматически считаются из **databases.config** - это поведение может быть изменено при помощи переменных окружения)

    python3 initialize.py
  
Заполнить базу данных значениями, если они были заранее сгенерированы

    python3 fill.py
  
В противном случае сначла сгенерировать значения (следующая команда запускается из папки **generators**)
  
    python3 main.py
  
В скрипте можно изменять объем данных для генерации
  
Далее можно проверить что все прошло успешно запуском ряда простых манипуляций с данными

    python3 explore.py
  
## Communications

### Entities

* person - представление члена экипажа в рамках графической модели данных

|property|data type|description|
|--------|---------|-----------|
|id|two ints|Идентификатор члена экипажа, соответствующий 12 - байтному идентификатору в базе данных, содержащей информацию о корабле (основанной на Mongo DB)|
|controlled|reference|Связь с сущностью Department, отображающая отношение главенствования над департаментом (DIRECTOR)|
|executor|reference|Связь с сущностью Operation, отображающая отношение исполнения операции (EXECUTOR)|
|headed|reference|Связь с сущностью Operation, отображающая отношение руководства операцией (HEAD)|
|worker|reference|Связь с сущностью Shift, отображающая отношение рядового участника смены (WORKER)|
|chief|reference|Связь с сущностью Shift, отображающая отношение ответственного за смену (CHIEF)|

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

### pymongo

Модуль для python, с помощью которого идет взаимодействие с базой данных, содержащей информацию о корабле (работающей на технологии Mongo DB) для обеспечения консистентности хранимых данных при их изменении

Устанавливается командой 
    
    pip install pymongo

Значения в базе данных neo4j, соответствующие индексам mongodb хранятся в виде пар значений целочисленного типа. Для перевода такой пары обратно в 12-байтный индекс, необходимы вычислить значение

    item[0] * 2^48 + item[1]

И интерпретировать его как 12-байтный индекс

Например, если имеем mongo - идентификатор

    5abfdba6ee6b7f5eec83a1ca

То можем его отобразить в целочисленном представлении

    28085592993066680294893134282

Или, если разбить на два числа, то получится

    (99780070403691, 140045671702986)

Обратное преобразование выглядит как

    (int(math.pow(2, 48)) * 99780070403691 + 140045671702986).to_bytes(12, byteorder='big').hex()
  
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

  
