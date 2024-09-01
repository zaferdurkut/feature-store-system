FROM python:3.9

COPY requirements.txt ./
RUN pip install  -r requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
COPY application_start.sh /application_start.sh
RUN chmod +x /application_start.sh
COPY . /app
WORKDIR /app
