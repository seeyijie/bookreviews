import boto3
import logging
import fire
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None, ExtraArgs={'ACL': 'public-read'}):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def cli(data_file):
    upload_file(data_file, "50043-analytics")

if __name__ == '__main__':
  fire.Fire(cli)
