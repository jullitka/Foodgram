# Проект "Продуктовый помощник"
![example workflow](https://github.com/jullitka/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Онлайн-сервис "Продуктовый помощник" дает возможность публиковать свои рецепты и просматривать рецепты других пользователей, формировать список необходимых ингредиентов из понравившихся рецептов и скачивать его. Доступна регистрация и авторизация пользователей.

## Возможности:
- Регистрация на сайте
- Публикация рецептов
- Просмотр рецептов других пользователей
- Подписка на других пользователей
- Добавление понравившизся рецептов в избранное
- Формирование продуктовой корзины
- Получение списка необходимых продуктов в виде файла

## Стек технологий:
- Python 3.7
- Django REST framework
- Django ORM
- Docker
- Gunicorn
- nginx
- PostgreSQL
- GIT



### Клонирование репозитория

```
git clone https://github.com/jullitka/foodgram-project-react.git
```
### Запуск проекта в контейнерах
- Перейдите в директорию /infra
- Cоздайте файл .env, с переменными окружения, используя образец:
```
SECRET_KEY = <secret_key>
ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = localhost
DB_PORT = 5432
```

- Соберите контейнеры
```
docker-compose up -d --build
```
- Выполните миграции
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
- Соберите статику
```
docker-compose exec backend python manage.py collectstatic
```
- Создайте суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```
- Наполните базу данных ингредиентами
```
docker-compose exec backend python manage.py import_ingredients
```

## API

Базовый url
```
api/
```
Добавляйте базовый url перед конечными точками.

Просматривать рецепты  и страницы пользователей могут любые пользователи.

Создавать, редактировать и удалять свои рецепты, добавлять другие рецепты в избранное, подписываться на других пользователей и формировать список покупок могут авторизованные пользователи.

### Пример запроса

Создание рецепта.

POST-запрос к /recipes/
#### Запрос

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw<...>",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
#### Ответ
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
