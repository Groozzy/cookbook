# Foodgram

Этот проект представляет собой веб-сайт, который позволяет пользователям делиться своими любимыми рецептами блюд, подписываться друг на друга, сохранять рецепты в избранное и генерировать список покупок на основе интересующих их рецептов.

## Цель проекта

Цель этого проекта — создать платформу, где люди могут легко обмениваться рецептами и находить новые идеи для приготовления еды.

## Функциональность

1. Регистрация и авторизация пользователей
2. Добавление новых рецептов с возможностью прикрепления фото и пошаговых инструкций
3. Просмотр рецептов других пользователей
4. Подписка на других пользователей
5. Сохранение рецептов в избранное
6. Генерация списка покупок на основе выбранных рецептов


## Запуск проекта

- Склонируйте репозиторй

```text
git@github.com:Groozzy/foodgram-project-react.git
```

- Подключитесь к серверу:

```text
ssh <server user>@<server IP>
```

- Установите Docker на сервер

```text
sudo apt install docker.io
```

- Установите Docker compose

```text
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

- Получите права для docker-compose

```text
sudo chmod +x /usr/local/bin/docker-compose
```

- Создайте директорию проекта

```text
mkdir foodgram && cd foodgram/
```

- Сойздайте env-файл:

```text
touch .env
```

- Заполните env-файл следующим образом:

```text
DEBUG=False
SECRET_KEY=<Секретный ключ из settings.py>
ALLOWED_HOSTS=<Хост>
CSRF_TRUSTED_ORIGINS=https://<домен>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Пароль>
DB_HOST=foodgram-db
DB_PORT=5432
```

- Скопируйте файлы из 'infra/' на своём ПК на сервер:

```text
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```

- Запустите docker-compose

```text
sudo docker-compose -f docker-compose.production.yml up -d
```

**Дополниетльно**

Создайте суперпользователя

```text
sudo docker exec -it app python manage.py createsuperuser
```

Залейте в БД список ингредиентов:

```text
sudo docker compose -f docker-compose.production.yml exec backend python manage.py uploadingredients
```