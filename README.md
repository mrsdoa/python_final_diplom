**Установка и запуск**

Склонируйте репозиторий с github: <[https://github.com/mrsdoa/python_final_diplom.git](https://github.com/mrsdoa/python_final_diplom.git)>

Для запуска проекта выполните команду из директории проекта:
docker-compose up -d --build

Выполните миграции внутри контейнера:
docker-compose run django python manage.py migrate

Для последующих запусков используйте команду:
docker-compose up -d

Приложение доступно на локальном сервере по адресу:
(<u>! важно</u> - проверьте, что у вас не запущены другие приложения на порту 8000)
http://127.0.0.1:8000/
