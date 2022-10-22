import boto3
import os
import json

os.environ['AWS_PROFILE'] = "baadal"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def add_item(info):
    table = dynamodb.Table('student_info')
    response = table.put_item(Item=info)
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    print(status_code)

with open('student_data.json') as json_file:
    students = json.load(json_file)
    for student in students:
        response = add_item(student)