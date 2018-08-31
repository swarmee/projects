FROM python:latest

RUN mkdir -p /home/project/search-frontend
WORKDIR /home/project/search-frontend
COPY requirements.txt /home/project/search-frontend
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/project/search-frontend

