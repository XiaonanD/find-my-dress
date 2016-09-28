import boto3

from findmydress.web import config


session = boto3.Session(profile_name=config.AWS_PROFILE)
s3_client = session.client('s3')
