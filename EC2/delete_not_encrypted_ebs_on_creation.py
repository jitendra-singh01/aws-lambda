import json
import boto3
from arnparse import arnparse
def lambda_handler(event, context):
    is_delete = False
    if "detail" in event and 'source' in event and event['source']== "aws.ec2" and "event" in event['detail']:
        event_type = event['detail']['event']
        
        result = event['detail']['result']
        if(event_type == "createVolume" and result == "available"):
            vol_arn = event['resources'][0]
            sns = boto3.client('sns')
            if len(event['resources']) == 1:
                vol_arn = event['resources'][0]
                vol_arn = arnparse(vol_arn)
                ec2 = boto3.resource('ec2', region_name=vol_arn.region)
                volume = ec2.volumes.filter(Filters=[{'Name': 'volume-id', 'Values': [vol_arn.resource]}])
                for vol in volume:
                    if not vol.encrypted:
                        is_delete = True
                        vol.delete()
                if is_delete == True:
                    response = sns.publish(
                        TopicArn="arn:aws:sns:us-east-1:002838516900:Sendnotification",    
                        Subject= "Deleted Volume -" + vol_arn.resource,
                        Message="Volume was not encrypted"
                    )
                return {"result":1}
            else:
                return {"error":1}
        else:
            return {"error":1}
    else:
        return {"error":1}
