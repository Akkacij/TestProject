# pull official base image
FROM python:3.8
# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput