''' Creates Layer Between ENV Variables and Environment Values Used in Application '''

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

WBE_SECRETKEY = os.environ['WBE_SECRETKEY']
WBE_DEBUG = os.environ['WBE_DEBUG']
WBE_ALLOWED_HOSTS = os.environ['WBE_ALLOWED_HOSTS']
AZURE_STORAGE_ACCESS_KEY = os.environ['AZURE_STORAGE_ACCESS_KEY']
AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

DB_ENGINE = os.environ['DB_ENGINE']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_DRIVER = os.environ['DB_DRIVER']