# World_of_recipes -  это ресурс для публикации рецептов.  
## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
## Описание проекта
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в pdf формате
## Список рецептов 
![Recipes](https://github.com/DmitriiParshin/world_of_recipes/raw/master/image/recipes.png)
## Подписки на авторов
![Subscription](https://github.com/DmitriiParshin/world_of_recipes/raw/master/image/subscription.png)
## Создание рецепта
![Create_recipe](https://github.com/DmitriiParshin/world_of_recipes/raw/master/image/create_recipe.png)
## Избранные рецепты
![Favorite](https://github.com/DmitriiParshin/world_of_recipes/raw/master/image/favorite.png)
## Список покупок
![Shopping_cart](https://github.com/DmitriiParshin/world_of_recipes/raw/master/image/shopping_cart.png)
_______________________________________________________________________________
## Запуск проекта
1. Клонируйте репозиторий с проектом и перейдите в каталог с ним:
```
git clone https://github.com/DmitriiParshin/world_of_recipes
cd world_of_recipes
```
2. Создайте файл `.env` и заполните его как показано на примере:
```
touch .env
```
>_DB_ENGINE=YOUR_DB_ENGINE  
DB_NAME=YOUR_DB_NAME  
DB_USER=YOUR_DB_USER  
DB_PASSWORD=YOUR_DB_PASSWORD  
DB_HOST=YOUR_DB_HOST  
DB_PORT=YOUR_DB_PORT_  

3. Перейти в директорию `infra/`и запустите контейнеры:
```
cd infra/
sudo docker-compose up -d --build
```
4. Создайте и выполните миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```
5. Соберите статику и загрузите ингредиенты и тэги:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py load_tags
sudo docker-compose exec backend python manage.py load_ingrs
```
6. Создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Перейдите на http://localhost/ и авторизуйтесь
_______________________________________________________________________________
## Автор
[Паршин Дмитрий](https://github.com/DmitriiParshin)