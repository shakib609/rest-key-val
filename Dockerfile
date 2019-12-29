FROM python:3-alpine

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV ALLOWED_HOSTS="localhost" \
    REDIS_HOST="redis"

ADD .  /usr/local/app/
WORKDIR /usr/local/app/
