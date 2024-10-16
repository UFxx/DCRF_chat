## Установка редиса и пакетов 

```
docker run -d -p 6379:6379 redis
```

```
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```
### После перейди в директорию backend

## Запуск сервера 

```
daphne -b 127.0.0.1 -p 8001 backend.asgi:application
```
