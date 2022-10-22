sudo docker build -t video-face-recognition .
/usr/local/bin/aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 693518781741.dkr.ecr.us-east-1.amazonaws.com
#/usr/local/bin/aws ecr create-repository --repository-name video-face-recognition --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
sudo docker tag video-face-recognition:latest 693518781741.dkr.ecr.us-east-1.amazonaws.com/video-face-recognition:latest
sudo docker push 693518781741.dkr.ecr.us-east-1.amazonaws.com/video-face-recognition:latest
