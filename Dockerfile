FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN export PATH="/home/user/.local/bin:$PATH"

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
