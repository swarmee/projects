FROM python:latest

RUN mkdir -p /home/project/suburb-api
WORKDIR /home/project/suburb-api 
COPY requirements.txt /home/project/suburb-api 
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/suburb-api 

