FROM python:3.11-slim

WORKDIR /app
RUN apt update \
    && apt upgrade -y\
    && apt install -y curl

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
