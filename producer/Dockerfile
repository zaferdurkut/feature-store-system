FROM python:3.9

COPY producer/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./.. /app
WORKDIR /app

RUN cd /app/
