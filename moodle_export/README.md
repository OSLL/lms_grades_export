# Grades Parser

## Инструкция по запуску скрипта.

Сначала следует установить все необходимые зависимости: 

``` pip3 install -r requirements.txt ```

Чтобы получить данные в файл grades.csv следует прописать:

``` python3 grades_parser.py --moodle_token 0b2eb395e25be56359d3b1f2cd36eed0 --url http://e.moevm.info --course_id 64 --csv_path grades.csv ```

Если хотите получить не баллы за задания, а проценты, то нужно добавить параметр ``` --percentages ```.

Получение данных и в файл и в Google таблицу:

``` python3 grades_parser.py --moodle_token 0b2eb395e25be56359d3b1f2cd36eed0 --url http://e.moevm.info --course_id 64 --csv_path grades.csv --google_token gradesparser-9f129ced5603.json --table_id 1J0xIhCYRRVQE7UgGDR3G7cGl_5KAo64Nh50fmfOFpOM --sheet_id grades ```

Получение ``` .json ``` файла для google_token будет описано ниже.

## Инструкция по сборке и запуску Docker контейнера.

Убедитесь, что вместе с исходным кодом лежит ``` .json ``` файл, необходимый для google_token.

Создание докер образа:

``` docker build --tag grades_parser . ```

Запуск докер контейнера с параметрами:

``` docker run --rm grades_parser --moodle_token 0b2eb395e25be56359d3b1f2cd36eed0 --url http://e.moevm.info --course_id 64 --csv_path grades.csv --google_token gradesparser-9f129ced5603.json --table_id 1J0xIhCYRRVQE7UgGDR3G7cGl_5KAo64Nh50fmfOFpOM --sheet_id grades ```


## Получение Moodle Токена.

Не являясь администратором можно получить токен отправив запрос с указанием логина, пароля и названием сервиса (за неимением которого можно выставить moodle_mobile_app):

``` https://www.yourmoodle.com/login/token.php?username=USERNAME&password=PASSWORD&service=moodle_mobile_app ```

Инструкция написана на [сайте](https://docs.moodle.org/dev/Creating_a_web_service_client).

## Получение токена для работы с Google таблицей.

Сначала нужно создать проект на сайте [Google Cloud](https://console.cloud.google.com/). Выбираем название проекта, жмем на кнопку "Create". 

Затем в меню слева нажимаем на API'S & Services, выбираем Enabled APIs & services. Затем на новой страничке сверху находим "+" с надписью ENABLE APIS AND SERVICES. В поиске находим sheet, нажимаем на кнопку enable, такое же можно сделать и для drive. Теперь приложение может общаться с помощью API Google sheets.

В меню слева в API'S & Services переходим на вкладку Credentials, сверху должен быть восклицательный знак в оранжевом треугольнике, в этом сообщении нажимаем на CONFIGURE CONSENT SCREEN. Выбираем external и жмем Create. Заполняем поля со звездочками, жмем SAVE AND CONTINUE. 

Заходим опять в Credentials. Нажимаем сверху на "+" CREATE CREDENTIALS и выбираем Service account. На первом этапе создаем имя,;жмем continue, на втором даем себе права owner, жмем DONE.

В таблице Service Accounts будет запись, нажимаем на нее. Сверху будет вкладка keys. Add key -> Create new key -> json -> create. Получаем нужный json файл.

## Как подключиться к таблице, которая может дать права редактора для определенной почты.

В полученном json файле есть почта некоторого формата, если в гугл таблице дать право редактора этой почте, приложение будет сохранять данные в таблицу.

