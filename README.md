# Foodgram

### Описание проекта

Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.

### Технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Реализация CI/CD

- Приложение возможно запустить как локально, так и на сервере.
- Для этого вам помогут docker compose файлы
```text
infra/docker-compose-production.yml - Запуск на сервере
infra/docker-compose-local.yml - Запуск на локальной машине
```

### Запуск проекта на удаленном сервере.

- Скачайте проект
```bash
git clone https://github.com/PROSHANTI/foodgram.git
```

- Скопируйте содержимое папки  ``infra/`` на удаленный сервер
```bash
cd foodgram
scp -r infra/* user@ip_host:/home/user/foodgram/infra
```
- Зайдите на удаленный сервер
```bash
ssh user@ip 
```
- Установите Docker
```bash
sudo apt install docker.io 
```
- Запустите сборку и развертывание образов
```bash
cd foodgram/infra
sudo docker compose -f docker-compose-production.yml up -d --build 
```
- Создайте миграции, примините их, соберите статику и импортируйте инградиенты, а так же создайте суперпользователя
```bash
sudo docker compose -f docker-compose-production.yml exec backend python manage.py makemigrations --noinput
sudo docker compose -f docker-compose-production.yml exec backend python manage.py migrate --noinput
sudo docker compose -f docker-compose-production.yml exec backend python manage.py collectstatic --noinput
sudo docker compose -f docker-compose-production.yml exec backend python manage.py load_ingredients 
sudo docker compose -f docker-compose-production.yml exec backend python manage.py createsuperuser
```

### Сервер в интернете.
```text
Сервер развернут по адресу: http://foodgram.serveblog.net
Данные для ревьюера:
Login: reviewer
passwod: P@ssw0rd
```

### Автор проекта

Максим Субботин - [GitHub](<https://github.com/PROSHANTI>)