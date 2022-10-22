import os
import pickle
import face_recognition
video_file_path = "/home/ubuntu/cse546-project-lambda/test_cases/test_case_1/test_0.mp4"
save_path = "/home/ubuntu/on_demand_video_analytics_aws/frames/"
encoding_path = "/home/ubuntu/cse546-project-lambda/encoding"

def save_frame(video_file_path, save_image_path):
    command = "ffmpeg -i " + str(video_file_path) + " -r 1 " + str(save_image_path) + "image-%3d.jpeg"
    print(command)
    os.system(command)

def process_frames_get_student_name(frames_path, encoding_path):
    with open(encoding_path, 'rb') as f:
        encodings = pickle.load(f)

    encoding_vals = encoding['encoding']
    for frame in sorted(os.listdir(frames_path)):
        print(frames_path+frame)
        image = face_recognition.load_image_file(frames_path+frame)
        face_encoding = face_recognition.face_encodings(image)[0]
        for encoding in encodings:
            face_match = face_recognition.compare_faces([face_encoding[1]], encoding_vals[0])
            print(face_match)
            if face_match[0]:
                return encodings['name'][encoding_vals[0]]
    return None

# save_frame(video_file_path, save_path)
# process_frames_get_student_name(save_path, encoding_path)