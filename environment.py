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
