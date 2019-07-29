import json
import boto3    
def lambda_handler(event, context):
    ec2client = boto3.client('ec2')
    result = {}
    client = boto3.client('ec2', region_name='us-east-1')
    #ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    ec2_regions = ['us-east-1']
    instances_with_no_stop_tags = []
    for region in ec2_regions:
	    conn = boto3.resource('ec2', region_name=region)
	    instances = conn.instances.filter(Filters=[{'Name':'tag:stop', 'Values':['1']}])
	    for instance in instances:
	        if instance['status']=="stop"
	        instances_with_no_stop_tags.append(instance)
            
    if(len(instances_with_no_stop_tags) > 0):
        for instance in instances_with_no_stop_tags:
            instance.terminate()
        result["success"] = 1
    else:
        result["error"] = 1
    return result
