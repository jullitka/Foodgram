# Проект "Продуктовый помощник"
![example workflow](https://github.com/jullitka/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Онлайн-сервис "Продуктовый помощник" дает возможность публиковать свои рецепты и просматривать рецепты других пользователей, формировать список необходимых ингредиентов из понравившихся рецептов и скачивать его. Доступна регистрация и авторизация пользователей.

## Возможности:
- Регистрация на сайте
- Незарегистрированные пользователи могут только просматривать рецепты.
- Публикация рецептов
- Просмотр рецептов других пользователей
- Подписка на других пользователей
- Добавление понравившизся рецептов в избранное
- Формирование продуктовой корзины
- Получение списка необходимых продуктов в виде файла

## Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

Документация доступна после запуска по адресу: http://localhost/api/docs/redoc.html.

## Запуск проекта

- Клонировать репозиторий

```
git clone https://github.com/jullitka/Foodgram.git
```
- Cоздать и активировать виртуальное окружение:

```
python -m venv env
```
Для Linux
    ```
    source venv/bin/activate
    ```
    
Для Windows
    ```
    source venv/Scripts/activate
    ```

- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск проекта на удаленном сервере с помощтю GitHub Actions

- #### Установить docker и docker-compose на удаленном сервере.
- #### Скопировать файлы docker-compose.yml и nginx.conf на удаленный сервер
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
- #### Добавить в Secrets репозитория проекта на github следующие переменные окружения:
```
HOST=<ip сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<приватный SSH-ключ>
DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль DockerHub>
USER=<username для подключения к удаленному серверу>
TELEGRAM_TO=<id Телеграм-аккаунта>
TELEGRAM_TOKEN=<токен бота>
```
- #### После выполнения команды git push запустится workflow:
- tests: проверка кода на соответствие PEP8.
- build_and_push_to_docker_hub: сборка и размещение образа проекта на DockerHub.
- deploy: автоматический деплой на сервер и запуск проекта.
- send_massage: отправка уведомления пользователю в Телеграм о том, что проект успешно запущен.

В случае успешного выполнения предыдущего пункта на сервере необходимо выполнить следующие команды:

- #### Выполнить миграции:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
- #### Собрать статику
```
docker-compose exec backend python manage.py collectstatic
```
- #### Создать суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```
- #### Наполнить базу данных ингредиентами
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

## Авторы
[Юлия Пашкова](https://github.com/Jullitka)

