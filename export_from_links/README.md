# developer.google.com badges Parser

## Инструкция по запуску скрипта

- --table_link - ссылка на таблицу формата https://docs.google.com/spreadsheets/d/{id}/edit? (важно наличие edit)
- --credentials - токен для загрузки на Яндекс диск
- --prefix_column_name - название колонки, которая будет использоваться как префикс для имен файлов
- --download_column_name - название колонки, которое будет добавлено после префикса в имени файла
- --cloud_directory_path - название директории, в которую загружать файлы на Яндекс Диск (может создать директорию, если это не подразумевает создание родительских директорий)

```bash
 python main.py --table_link https://docs.google.com/spreadsheets/d/{id}/edit? --credentials <yandex_disk_token> --prefix_column_name <Название колонки префиксов> --download_column_name <Название колонки с ссылками> --cloud_directory_path <Путь на диске>
```
