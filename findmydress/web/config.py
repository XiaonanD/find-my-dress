import os

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

# TODO: remove hard-coded facepalm here - move to config
IMAGE_FILES_ROOT = '/Users/dave/projects/modscrape/files/images'

STATIC_ROOT = os.path.join(APP_ROOT, 'static')
DATA_ROOT = os.path.abspath(os.path.join(APP_ROOT, '../../data'))

STATIC_LABELS = [
    "background",
    "mask",
    ]

AWS_PROFILE = 'findmydress-web'
DB_CONNECTION_STRING = 'postgresql+psycopg2://localhost/findmydress'
