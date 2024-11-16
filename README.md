# credit_approval_system
docker compose build

docker compose up

docker compose exec web python manage.py migrate 

docker compose logs celery

 => Test Celery Tasks

docker compose exec web python manage.py shell

from approval.tasks import load_customer_data, load_loan_data
load_customer_data.delay()
load_loan_data.delay()


=>Test api in postman:

postman collection-https://dark-shuttle-316146.postman.co/workspace/New-Team-Workspace~2520c6ff-2b4c-429d-8afb-f76492bfc532/collection/29159995-663a3731-46b4-47cc-ad35-ebb0c282595c?action=share&creator=29159995https://dark-shuttle-316146.postman.co/workspace/New-Team-Workspace~2520c6ff-2b4c-429d-8afb-f76492bfc532/collection/29159995-663a3731-46b4-47cc-ad35-ebb0c282595c?action=share&creator=29159995

Notion : 
https://salty-ocelot-f2a.notion.site/Alemeno-assignment-140ae96341b680708d39d82e15016f28
