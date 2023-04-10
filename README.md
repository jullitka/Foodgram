# Проект "Продуктовый помощник"

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



## Клонирование репозитория

```
git clone https://github.com/jullitka/foodgram-project-react.git
```
## Виртуальное окружение
```
python -m venv venv
```
Активируем виртуальное окружение
- Linux:
```
source venv/bin/activate
```
- Windows:
```
source venv/Scripts/activate
```
Устанавливаем зависимости:
```
python -m pip install --upgrade pip
pip install -r backend/foodgram/requirements.txt
```

## API
Базовый url
```
api/
```
Добавляйте базовый url перед конечными точками.

Базовый url
```
api/
```
Добавляйте базовый url перед конечными точками.

Просматривать рецепты  и страницы пользователей могут любые пользователи.

Создавать, редактировать и удалять свои рецепты, добавлять другие рецепты в избранное, подписываться на других пользователей и формировать список покупок могут авторизованные пользователи.

### Примеры запросов
