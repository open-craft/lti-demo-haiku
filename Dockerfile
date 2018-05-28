FROM python:2.7.15-wheezy

COPY . /var/app/
WORKDIR /var/app/
RUN apt-get update && apt-get install -y git
ENV SECRET_KEY=abracadabra LTI_CLIENT_KEY=opensesame LTI_CLIENT_SECRET=poweroverwhelming PASSWORD_GENERATOR_NONCE=seasalt
RUN pip install -r requirements/base.txt
RUN python ./manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
EXPOSE 8080

ENTRYPOINT ["python", "./manage.py", "runserver", "0.0.0.0:8080"]
