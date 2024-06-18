# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Import env vars.
ARG DEBUG
ARG ENVIRONMENT
ARG DATABASE_NAME
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG DATABASE_HOST
ARG DATABASE_PORT
ARG DJANGO_SECRET_KEY
ARG SUPABSE_DB_NAME
ARG SUPABASE_DB_PORT
ARG SUPABASE_DB_USER
ARG SUPABASE_DB_PASSWORD
ARG SUPABASE_DB_HOST


# Update the package lists and install required system packages
RUN apt-get update

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file into the container
COPY requirements.txt /code/

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /code/

# Set environment variables
ARG PORT=80
ENV PORT=${PORT}

# Add the docker-entrypoint.sh script and set permissions
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

# Set the entrypoint and default command
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD uvicorn social_network.asgi:application --host 0.0.0.0 --port ${PORT} --log-config log_config.json --timeout-keep-alive 300
