
# Онлайн школа с использованием Django и Django REST Framework

Этот проект представляет собой онлайн школу, созданную с использованием Django и Django REST Framework. Он позволяет пользователям просматривать курсы, уроки, а также редактировать свой профиль.

## Установка

1. Клонируйте репозиторий на свой компьютер:

    ```bash
    git clone https://github.com/your_username/drf_online_school.git
    ```

2. Установите зависимости с помощью poetry:

    ```bash
    poetry install
    ```

3. Примените миграции:

    ```bash
    poetry run python manage.py migrate
    ```

4. Запустите сервер:

    ```bash
    poetry run python manage.py runserver
    ```

## Использование

### Эндпоинты API

- `/api/courses/`: Получить список всех курсов или создать новый курс.
- `/api/courses/<id>/`: Получить, обновить или удалить курс с определенным идентификатором.
- `/api/lessons/`: Получить список всех уроков или создать новый урок.
- `/api/lessons/<id>/`: Получить, обновить или удалить урок с определенным идентификатором.
- `/api/profile/`: Получить список всех пользователей или создать нового пользователя.
- `/api/profile/<id>/`: Получить, обновить или удалить пользователя с определенным идентификатором.

### Аутентификация

API не требует аутентификации для просмотра данных, но для редактирования профиля пользователя требуется аутентификация.

### Тестирование

Для запуска тестов используйте команду:

```bash
poetry run python manage.py test
```

## Дополнительные возможности

- Поддержка аутентификации и авторизации пользователей.
- Валидация данных с использованием сериализаторов Django REST Framework.
- Обработка ошибок и исключений для более гибкого и устойчивого API.
- Документация API с помощью Swagger или ReDoc.
- Оптимизация производительности и масштабирование приложения.
- Логирование действий пользователей и событий в приложении.

## Автор

Проект разработал [Евгений Ермак](https://github.com/EvgeniiErmak).
