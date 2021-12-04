FROM python:3.8
RUN apt update
RUN apt install -y redis
RUN apt clean -y
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/www/lister
WORKDIR /var/www/lister
COPY requirements.txt /var/www/lister
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /var/www/lister
