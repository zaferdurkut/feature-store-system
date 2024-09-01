FROM docker.io/bitnami/spark:3-debian-10

# Switch to root stream
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

# Copy the requirements.txt file into the Docker image
COPY batch/requirements.txt /opt/spark-apps/requirements.txt

# Install Python packages from requirements.txt
RUN pip3 install -r /opt/spark-apps/requirements.txt

# Set environment variables for PySpark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
