import os

import boto3

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

STATIC_ROOT = os.path.join(APP_ROOT, 'static')
DATA_ROOT = os.path.abspath(os.path.join(APP_ROOT, '../../data'))
MATCHING_MODEL_PATH = os.path.join(DATA_ROOT, 'knn6.2016.09.24.pkl')

STATIC_LABELS = [
    "background",
    "mask",
    ]

AWS_PROFILE = 'findmydress-web'
DB_CONNECTION_STRING = 'postgresql+psycopg2://findmydress:Ooheum7hai2v@localhost/findmydress'
IMAGES_S3_BUCKET = 'findmydress'


def get_aws_session():
    return boto3.Session(profile_name=AWS_PROFILE)

def get_s3_connection():
    return get_aws_session().client('s3')
