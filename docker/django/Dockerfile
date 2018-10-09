FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app
COPY . /app

RUN pip install -r requirements.txt

COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh