# Use the official Airflow image as a base
FROM apache/airflow:2.5.1

# Copy requirements.txt to the Docker image
COPY airflow/requirements.txt /requirements.txt

# Install the Python packages
RUN pip install -r /requirements.txt

USER root

RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/opt/spark

# Ensure that java command is in PATH
ENV PATH $JAVA_HOME/bin:$PATH

# Copy entrypoint script into the container
COPY airflow/entrypoint.sh ./entrypoint.sh

RUN ["chmod", "755", "./entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]


# Switch back to airflow stream
USER airflow


# Command to start the webserver (or any other command)
CMD ["airflow", "webserver"]

