# Тестовое задание для Emphasoft

## Задание
Сделайте CRUD для юзеров с токен аутентификацией. [Пример](https://emphasoft-test-assignment.herokuapp.com/swagger/). \
Опционально: тесты, линтер и статическая типизация

## Решение
Для демонстрационных целей `db.sqlite3` и `settings.py` **не** добавлял в `.gitignore`. \
Использовал DRF. \
В [сериалайзерах](/crud/serializers.py) добавил поля только для чтения (`last_login`, `is_superuser`), \
поля только для записи (`password`) и обязательные поля (`username`, `password`, `is_active`).

### `views.py`
[Class based views](https://github.com/WannaFight/crud-token/blob/52c7616c32d952c5c126499c2c811ffffbfcdaba/crud/views.py) -> [mixins](https://github.com/WannaFight/crud-token/blob/e6da698c4581b8aab919f16f2db53b89db67e2e4/crud/views.py) -> [generics](https://github.com/WannaFight/crud-token/blob/a4d51e1c74c55ea33d6e2736fed9757d26833de9/crud/views.py) (current)

Также при DELETE добавил проверку:
```python
if kwargs['pk'] == request.user.pk:
    return Response(
        {'detail': "You can not delete yourself."},
        status=status.HTTP_409_CONFLICT
    )
```
Таким образом пользователь не может удалить сам себя через запрос к API.
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
