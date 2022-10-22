import os
import pickle
import face_recognition
import boto3
import credentials

save_path_video = "/tmp/"
save_path_frames = "/tmp/"

encoding_path = "/home/app/encoding"

region = credentials.region
aws_access_key_id = credentials.aws_access_key_id
aws_secret_access_key = credentials.aws_secret_access_key
s3_client = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def save_frame(video_key):
    video_file_path = save_path_video + video_key
    command = "ffmpeg -i " + str(video_file_path) + " -r 1 " + str(save_path_frames) + "image-%3d.jpeg"
    os.system(command)

def download_video(input_bucket, item_name):
    s3_client.download_file(input_bucket, item_name, str(save_path_video) + item_name)

def process_frames_get_student_name():
    with open(encoding_path, 'rb') as f:
        encodings = pickle.load(f)

    encoding_vals = encodings['encoding']
    #print(f"encoding_vals={encoding_vals}")
    frame = save_path_frames + 'image-001.jpeg'
    print(frame)
    image = face_recognition.load_image_file(frame)
    if image is None:
        print("Could not load frame")
    face_encoding = face_recognition.face_encodings(image)[0]
    if face_encoding is None:
        print("Could not create face encoding")
    else:
        tp = type(face_encoding)
        print(f"face encoding of type {tp} created.")
    matches = face_recognition.compare_faces(encoding_vals, face_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        return encodings['name'][first_match_index]            
    return None