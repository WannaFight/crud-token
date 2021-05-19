# Тестовое задание для Emphasoft

## Задание
Сделайте CRUD для юзеров с токен аутентификацией. [Пример](https://emphasoft-test-assignment.herokuapp.com/swagger/). \
Опционально: тесты, линтер и статическая типизация

## Решение
Для демонстрационных целей `db.sqlite3` и `settings.py` **не** добавлял в `.gitignore`. \
Использовал DRF. \
В [сериалайзерах](/crud/serializers.py) добавил поля только для чтения (`last_login`, `is_superuser`), \
поля только для записи (`password`) и обязательные поля (`username`, `password`, `is_active`).


## Как запустить
```shell
~$ git clone ... && cd emphasoft_test
~$ python -m venv env
~$ pip install -r requirements.txt
~$ ./manage.py runserver
```
Admin Account (admin:1234)

## Как получить токен
```shell
~$ token=$(curl -X POST localhost:8000/api-token-auth/ --data "username=admin&password=1234" | jq -r ".token")
~$ token=$(python manage.py drf_create_token admin | awk '{print $3}')
```
