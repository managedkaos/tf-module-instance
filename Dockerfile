# Use an official Python runtime as a parent image
FROM python:3.12-slim
ENV PROJECT_HOME=/data
RUN mkdir /data

# Set the working directory in the container
WORKDIR /usr/local/bin

# Copy the script into the container at /usr/src/app
COPY ./script.py /usr/local/bin/

# Run the script when the container launches
ENTRYPOINT ["python", "/usr/local/bin/script.py"]
