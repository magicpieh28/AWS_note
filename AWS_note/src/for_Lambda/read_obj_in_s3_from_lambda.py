import json
import boto3


def read_obj_in_s3(bucket_name: str, obj_key: str):
    return boto3.resource('s3').Object(
        bucket_name,
        obj_key
    ).get()['Body'].read()
