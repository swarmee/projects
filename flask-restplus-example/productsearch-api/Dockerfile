FROM python:latest

RUN mkdir -p /home/project/productSearch-api
WORKDIR /home/project/productSearch-api
COPY requirements.txt /home/project/productSearch-api
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/productSearch-api

