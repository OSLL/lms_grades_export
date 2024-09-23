# developer.google.com badges Parser

## Инструкция по запуску скрипта

- -o | --output - название выходного csv файла
- -i | --ids_file - список id пользователей (файл c id разделенные переносами строки)
- -k | --key - ключ (брал из dev консоли браузера в запросе)
- -t | --timeout - таймаут 1 запроса

```bash
python3 main.py -i 'ids' -o 'fname.csv' -k 'ключ' -t 0.1
```
