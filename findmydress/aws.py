import boto3

from findmydress import config


def get_aws_session():
    return boto3.Session(profile_name=config.AWS_PROFILE)


def get_s3_connection():
    return get_aws_session().client('s3')
