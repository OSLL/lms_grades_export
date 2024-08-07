# Выгрузка истории прохождения по курсу Stepik

Скрипт, выгружающий время, когда студент решил каждую задачу в курсе на stepik.

Можно использовать, чтобы определять людей, которые скопипастили все решения и прошли курс за один день.

## Использование

Запуск: `python main.py` или `docker-compose run parser`

Аргументы:
- `client_id`, `client_secret` - параметры OAuth (https://stepik.org/oauth2/applications/)
- `course_id` - ID курса (отсюда: https://stepik.org/course/63054/syllabus)
- `class_id` - ID класса (отсюда: https://stepik.org/class/33587/gradebook)
- `csv_path` - путь до CSV
- `yandex_token` - токен доступа Yandex App (отсюда: https://oauth.yandex.ru/client/new)
- `yandex_path` - путь до CSV на Диске

Например:
```bash
docker-compose run parser --client_id xxx --client_secret xxx --course_id 63054 --class_id 33587 --csv_path ./results/kek.csv --yandex_token xxx --yandex_path kek.csv
```

Будет создан CSV-файл со следующим форматов:
1. `user_id`
2. `score` - Оценка человека по курсу
3. `date_joined` - Дата присоединения
4. `uniq_dates` - Количество дней, в которых человек решил хотя бы одну задачу
5. `start_date` - Когда человек начал решать курс
6. `end_date` - Когда закончил решать курс
7. `days` - `end_date` - `start_date` (дни)  

8..N `id шага` - дата успешного решения шага (YYYY-MM-DD)

По небольшому числу `uniq_dates` можно поискать обманщиков.

## Ограничения
Сложность по числу запросов: o(n * m), где n - число студентов, m - число шагов в курсе

## Что ещё сделать
1. М.б. будет интересно по времени решения задач определить людей, аномально быстро решающих задачи, но распределяющие решения по дням
2. Скачать все решения и проверить на плагиат
