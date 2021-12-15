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
    && apk add --no-cache gcc musl-dev libffi-dev zlib-dev jpeg-dev curl bash unixodbc-dev \
    && touch ~/.bashrc


# sudo su
# curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# #Download appropriate package for the OS version
# #Choose only ONE of the following, corresponding to your OS version

# #Ubuntu 20.04
# curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# exit
# sudo apt-get update
# sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# # optional: for bcp and sqlcmd
# sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
# echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# source ~/.bashrc
# # optional: for unixODBC development headers
# sudo apt-get install -y unixodbc-dev

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