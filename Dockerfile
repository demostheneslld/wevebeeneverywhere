# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /wbe

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD /wbe/start_server.sh