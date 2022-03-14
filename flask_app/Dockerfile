FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app
ADD . /app

RUN apt-get update
RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
