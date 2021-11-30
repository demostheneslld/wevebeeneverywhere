# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /wbe

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install linux dependencies
RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev zlib-dev jpeg-dev curl bash \
    && touch ~/.bashrc

# install node dependencies
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash \
  && . /root/.nvm/nvm.sh \
  && nvm install 16

# install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD /wbe/scripts/start_server.sh