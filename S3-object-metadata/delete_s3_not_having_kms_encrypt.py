import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    is_delete = False
    if "detail" in event and 'source' in event and event['source']== "aws.s3" and "eventName" in event['detail']:
        if event['detail']['eventName'] == "CreateBucket":
            bucket_name = event['detail']['requestParameters']['bucketName']
            if bucket_name is not None and bucket_name != "":
                s3 = boto3.client('s3')
                bucket = boto3.resource("s3")
                bucket = bucket.Bucket(bucket_name)
                try:
                    enc = s3.get_bucket_encryption(Bucket=bucket_name)
                    rules = enc['ServerSideEncryptionConfiguration']['Rules']
                    if rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] != "aws:kms":
                        delete_bucket(bucket)
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                        delete_bucket(bucket)
                    else:
                        delete_bucket(bucket)
    return {"msg":1}

def delete_bucket(bucket):
    bucket.delete()
    response = sns.publish(TopicArn="arn of sns",Subject= "Deleted S3 -" + bucket_name,Message="S3 was not encrypted"
                    )
