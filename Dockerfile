##################################
### Set the Pytest environment ###
##################################
FROM python:3.9.0-alpine

# Set the working directory
WORKDIR /pdf/

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
# Install all dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the folder with the tests into the container
COPY src src/
COPY conf conf/

# Copy the waiter
RUN apk add bash
RUN apk add tk

# This Dockerfile hasn't got any CMD or ENTRYPOINT so it doesn't do anything by its own.
# Check docker-compose.yml to see an implementation of the image