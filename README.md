# Foodgram

### Описание проекта

Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.

### Технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Запуск проекта на удаленном сервере.

- Скачайте проект
```bash
git clone https://github.com/PROSHANTI/foodgram.git
```

- Создайте файл .env и заполните его своими данными. Перечень данных указан в корневой директории проекта в файле .env.example.
- Установите Docker
```bash
sudo apt install docker.io
```
- Установите docker-compose на сервер:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose 
```
- На сервере соберите docker-compose:
```bash
sudo docker-compose up -d --build 
```
- Соберите статические файлы:
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput 
```
- Примените миграции:
```bash
sudo docker-compose exec backend python manage.py migrate --noinput 
```
- Создайте суперпользователя Django:
```bash
sudo docker-compose exec backend python manage.py createsuperuser 
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