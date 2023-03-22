FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.lock.txt /build/requirements.txt
RUN pip install --no-cache-dir -r /build/requirements.txt
WORKDIR /srv
COPY . /srv/

EXPOSE 8000
