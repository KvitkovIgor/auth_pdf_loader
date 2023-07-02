##################################
### Set the Pytest environment ###
##################################
FROM python:3.9.0-alpine

# Set the working directory
WORKDIR /app/

# Install all dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY wait-for-it.sh /app/

# Install requirements
RUN apk add bash
RUN apk add tk
