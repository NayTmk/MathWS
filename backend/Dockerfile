FROM python:3.13-slim

RUN groupadd -r groupfastapi && useradd -r -g groupfastapi userfastapi

RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /mathws
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
USER userfastapi
