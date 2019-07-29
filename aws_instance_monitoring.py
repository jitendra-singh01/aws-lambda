import boto3
import json
from datetime import datetime, timedelta
def lambda_handler(event, context):
    cpu_uti_dict = []
    try:
        filtermetrics = ""
        percentcolumn = ""
        if "filtermetrics" in event:
            filtermetrics = event['filtermetrics']
        else:
            filtermetrics = "CPUUtilization"
        
        if filtermetrics == "NetworkIn" or filtermetrics == "NetworkOut":
            percentcolumn = "Bytes"
        else:
            percentcolumn = "Percent"
        seconds_in_one_day = 300  # used for granularity
        cloudwatch = boto3.client('cloudwatch','us-east-1')
    
        response = cloudwatch.get_metric_statistics(Namespace='AWS/EC2',Dimensions=[{'Name': 'InstanceId','Value': 'i-0910c24d7fe24b255'}],MetricName=filtermetrics,StartTime=datetime.now() - timedelta(hours=1),EndTime=datetime.now(),Period=seconds_in_one_day,Statistics=['Maximum'],Unit=percentcolumn)
        dp = response['Datapoints']
        
        dp = sorted(dp, key = lambda i: i['Timestamp']) 
        if(len(dp) > 0):
    	    for i in dp:
    		    cpu_uti_dict.append({"x":str(i['Maximum']*100),"y":str(datetime.timestamp(i['Timestamp']))[:-2]})
        else:
            cpu_uti_dict.append({"err":1})
    except:
        cpu_uti_dict.append({"err":1})
 
    return cpu_uti_dict
