FROM python:3.11-slim
LABEL authors="hbayraktepe"

WORKDIR /usr/src/app

RUN apt-get update -y

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "app.py"]
