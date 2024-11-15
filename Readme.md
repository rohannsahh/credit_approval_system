docker-compose build


docker-compose up




docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser


docker-compose logs celery
