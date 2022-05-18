# syntax=docker/dockerfile:1
FROM ubuntu:20.04
FROM python:3.8

RUN apt-get update
#RUN apt-get install tesseract
#RUN apt-get install tesseract-lang
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-eng
RUN apt-get install tesseract-ocr-kor
#RUN apt-get install clean
#RUN apt-get install autoremove

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000