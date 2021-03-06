#
![YaMDB workflow](https://github.com/FadeevDV/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


# YaMDB_final
### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Приложение написано на основе `fullREST` архитектуры на фреймворке `django-rest-framework`. База данных `postgresssql`.
<br><br>Проект доступен по адресу: http://130.193.50.182 <br>
Документация: http://130.193.50.182/redoc/

Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

### Как развернуть проект
## Установка на локальном компьютере
Приведенная ниже последовательность позволит развернуть проект на локальной машине для тестирования
### Установка Docker
Для запуска проекта необходима установка программ `docker` и `docker-compose`. https://docs.docker.com/engine/install/
### Запуск проекта (Lunux)  
1. Создайте на локальном ПК папку проекта yamdb_final командой `mkdir
 yamdb_final`
 
2. Склонируйте репозиторий в текущую папку командой 
`git clone https://github.com/FadeevDV/yamdb_final/ .` и перейдите в нее командой `cd yamdb_final`

3. Создайте файл `.env` командой `touch .env
` с переменными окружениями для работы с базой данных на основе шаблона
 для работы с базой данных:
 ```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
    
4.Запустите `docker-compose` командой sudo `docker-compose up -d`

Следующие шаги выполняет скрипт `entrypoint.sh
`, в случае ручного выполнения необходимо выполнить следующие команды

- Создайте миграции `sudo docker-compose exec web python manage.py migrate`

- Соберите статику проекта командой `sudo docker-compose exec web python
 manage.py collectstatic --no-input`

5.Создайте суперпользователя Django `sudo docker-compose exec web python
 manage.py createsuperuser`

6.Загрузите фикстуры (тестовые данные) в базу данных командой `sudo docker
-compose exec web python manage.py loaddata fixtures.json`

7.Запуск тестов (при желании)<br>
В терминале или командной строке перейдите в директорию проекта (она содержит этот readme файл) командой `cd [путь]` <br>
Установите пакет pytest командой `pip install -U pytest` подробнее https://docs.pytest.org/en/stable/getting-started.html
<br>Запустите тесторование командой `pytest`


После описанных выше действий проект будет доступен по адресу `http://127.0.0.1`
<br>Документация для работы с API будет доступна по адресу `http://127.0.0.1/redoc`
## Установка (деплой) на удаленном сервере
## Деплой с использованием git actions
Необходимо создать переменные окружения в вашем репозитории github
 в разделе `secrets`
```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь сервера
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
TELEGRAM_TO # ID телеграм-аккаунта (для оправки уведомления об успешном деплое)
TELEGRAM_TOKEN # Токен бота (для оправки уведомления об успешном деплое)
```
При каждом деплое будет происходить:
- проверка кода соответствие страндарту `pep8`
- выполнение тестов `pytest`
- сборка и обновление образа на сервисе `docker-hub`
- автоматический деплой на сервер, указанный в `secrets`
- отправка уведомления в телеграм
При необходимости изменения или добавления действий редактируйте файл `.github/workflows/yamdb_workflow.yml`. <br>
Файл `yamdb_workflow.yaml
` является копией и создан для проведения тестов `pytest`

### Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметром email на /auth/email/.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
- Пользователь отправляет запрос с параметрами email и confirmation_code на /auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- При желании пользователь отправляет PATCH-запрос на /users/me/ и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- Модератор — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.
- Администратор Django — те же права, что и у роли Администратор.

### Ресурсы YaMDB_final
- Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Связанные данные и каскадное удаление
- При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
- При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
- При удалении объекта категории Category не удалять связанные с этой категорией произведения (Title).
- При удалении объекта жанра Genre не удалять связанные с этим жанром произведения (Title).
- При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.

#### AUTH - Аутентификация
- GET Получение JWT-токена в обмен на email и confirmation code
  -  /api/v1/auth/token/
- POST Отправление confirmation_code на переданный email.
  -  /api/v1/auth/email/
    
#### USERS - Пользователи
- GET Получить список всех пользователей.
  -  /api/v1/users/
  -  Права доступа: Администратор
- POST Создание пользователя.
  -  /api/v1/auth/email/
  -  Права доступа: Администратор
- GET Получить пользователя по username.
  -  /api/v1/users/{username}/
  -  Права доступа: Администратор
- PATCH Изменить данные пользователя по username.
  -  /api/v1/users/{username}/
  -  Права доступа: Администратор
- DEL Удалить пользователя по username. 
  -  /api/v1/users/{username}/
  -  Права доступа: Администратор
- GET Получить данные своей учетной записи.
  -  /api/v1/users/me/
  -  Права доступа: Любой авторизованный пользователь
- PATCH Изменить данные своей учетной записи.
  -  /api/v1/users/me/
  -  Права доступа: Любой авторизованный пользователь
    
#### REVIEWS - Отзывы

- GET Получить список всех отзывов. 
  -  /api/v1/titles/{title_id}/reviews/
  -  Права доступа: Доступно без токена.
- POST Создать новый отзыв.
  -  /api/v1/titles/{title_id}/reviews/
  -  Права доступа: Аутентифицированные пользователи.
- GET Получить отзыв по id.
  -  /api/v1/titles/{title_id}/reviews/{review_id}/
  -  Права доступа: Доступно без токена.
- PATCH Частично обновить отзыв по id.
  -  /api/v1/titles/{title_id}/reviews/{review_id}/
  -  Права доступа: Автор отзыва, модератор или администратор.
- DEL Удалить отзыв по id.
  -  /api/v1/titles/{title_id}/reviews/{review_id}/
  -  Права доступа: Автор отзыва, модератор или администратор.

#### COMMENTS - Комментарии к отзывам

 - GET Получить список всех комментариев к отзыву по id.
   -  /api/v1/titles/{title_id}/reviews/{review_id}/comments/
   -  Права доступа: Доступно без токена.
 - POST Создать новый комментарий для отзыва.
   -  /api/v1/titles/{title_id}/reviews/{review_id}/comments/
   -  Права доступа: Аутентифицированные пользователи.
 - GET Получить комментарий для отзыва по id.
   -  /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   -  Права доступа: Доступно без токена.
 - PATCH Частично обновить комментарий к отзыву по id.
   -  /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   -  Права доступа: Автор комментария, модератор или администратор.
 - DEL Удалить комментарий к отзыву по id.
   -  /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   -  Права доступа: Автор комментария, модератор или администратор.
    
#### CATEGORIES - Категории (типы) произведений

  - GET Получить список всех категорий.
    -  /api/v1/categories/
    -  Права доступа: Доступно без токена
  - POST Создать категорию.
    -  /api/v1/categories/
    -  Права доступа: Администратор.
  - DEL Удалить категорию. 
    -  /api/v1/categories/{slug}/
    -  Права доступа: Администратор.
    
 #### GENRES - Категории жанров

  - GET Получить список всех жанров.
    -  /api/v1/genres/
    -  Права доступа: Доступно без токена
  - POST Создать жанр. 
    -  /api/v1/genres/
    -  Права доступа: Администратор.
  - DEL Удалить жанр.
    -  /api/v1/genres/{slug}/
    -  Права доступа: Администратор.
    
 #### TITLES - Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

  - GET Получить список всех объектов.
    -  /api/v1/titles/
    -  Права доступа: Доступно без токена
  - POST Создать произведение для отзывов.
    -  /api/v1/titles/
    -  Права доступа: Администратор.
  - GET Информация об объекте.
    -  /api/v1/titles/{titles_id}/
    -  Права доступа: Доступно без токена.
  - PATCH Обновить информацию об объекте.
    -  /api/v1/titles/{titles_id}/
    -  Права доступа: Администратор
  - DEL Удалить произведение. 
    -  /api/v1/titles/{titles_id}/
    -  Права доступа: Администратор.
    
 #### Информация по запросам
Запустите сервер.

Перейдите на http://localhost:8000/redoc/

## Использованные технологии
Django Rest Framework https://www.django-rest-framework.org/ <br>
Django https://www.djangoproject.com/ <br>
PostgreSQL https://www.postgresql.org/ <br>
Docker https://www.docker.com/ <br>

## Проект разработан:

#### Игорь Огий

Роль: TL, Developer;<br>
develop: приложение User<br>

#### Олег Гичан

Роль: Developer;<br>
develop: приложение Api: модели, вьюхи, пермишены, сериалайзеры, эндпоинты для Category, Genre, Title<br>

#### Дмитрий Фадеев

Роль: Developer;<br>
develop: приложение Api: модели, вьюхи, пермишены, сериалайзеры, эндпоинты для Review, Comment<br>
