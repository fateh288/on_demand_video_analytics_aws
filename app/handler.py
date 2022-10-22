import face_recognition
import pickle
import boto3
import csv
import urllib.parse
import video_utils
import os
import credentials

region = credentials.region
aws_access_key_id = credentials.aws_access_key_id
aws_secret_access_key = credentials.aws_secret_access_key

s3_client = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
dynamodb_client = boto3.resource('dynamodb', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


input_bucket = "videobucketforlambda"

output_bucket = "studentinfolambda"

save_path_info = "/tmp/"

student_info_table = dynamodb_client.Table('student_info')

def write_info(file_name, name, major, year):
    
    file_csv = file_name.split('.')[0] + '.csv'
    with open(save_path_info + file_csv, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow([name, major, year])
    s3_client.upload_file(save_path_info + file_csv, output_bucket, file_csv)

def get_student_info(student_name):
	student_data = student_info_table.get_item(Key={'name': student_name})['Item']
	return [student_data['name'], student_data['major'], student_data['year']]

def face_recognition_handler(event, context):
		
	for record in event['Records']:
		# bucket = record['s3']['bucket']['name']
		key = urllib.parse.unquote_plus(record['s3']['object']['key'])
		print("input key=",key)
		video_utils.download_video(input_bucket, key)
		video_utils.save_frame(key)
		name = video_utils.process_frames_get_student_name()
		if name is not None:
			info = get_student_info(name)
			write_info(key, info[0], info[1], info[2])