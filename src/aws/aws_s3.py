import json
import os

import boto3

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

def getAbiFromS3(s3Key):

    fullPath = f"abis/{s3Key}"

    s3 = boto3.resource('s3')
    s3Bucket = os.getenv("S3_BUCKET")

    obj = s3.Object(s3Bucket, fullPath)
    abi = json.load(obj.get()['Body'])

    return json.dumps(abi)


