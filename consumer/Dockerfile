FROM python:3.9.18-bullseye

ARG FLINK_VER=1.18.1
ARG POETRY_VER=1.6.1

RUN apt update -y \
    && apt-get install -y --no-install-recommends \
    openjdk-11-jdk=11.0.* \
    && pip install poetry==$POETRY_VER \
    && mkdir -p /app /jars /flink \
    && wget -O /flink/flink.tgz https://dlcdn.apache.org/flink/flink-$FLINK_VER/flink-$FLINK_VER-bin-scala_2.12.tgz \
    && tar -C /flink --strip-components 1 -zxvf /flink/flink.tgz \
    && rm /flink/flink.tgz

COPY consumer/requirements.txt ./
RUN pip install -r requirements.txt

COPY consumer/flink-conf.yaml /opt/flink/conf/flink-conf.yaml
COPY ./.. /app
WORKDIR /app


ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64/

ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.1-1.18/flink-sql-connector-kafka-3.0.1-1.18.jar /jars


RUN cd /app/

