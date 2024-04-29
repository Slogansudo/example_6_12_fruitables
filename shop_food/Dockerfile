FROM python:3.10.12-alpine

WORKDIR /app

COPY requirement.txt requirement.txt

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

COPY .. .