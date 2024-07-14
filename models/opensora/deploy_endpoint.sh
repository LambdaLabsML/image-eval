#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error occurred in script at line: $1"
    exit 1
}

# Trap errors
trap 'handle_error $LINENO' ERR

# Variables
OPEN_SORA_REPO="https://github.com/hpcaitech/Open-Sora.git"
IMAGE_EVAL_REPO="https://github.com/LambdaLabsML/image-eval.git"

# Ensure required directories exist
echo "Checking required directories..."
if [ -d "/home/ubuntu/data" ]; then
    echo "Removing existing /home/ubuntu/data directory..."
    sudo rm -rf /home/ubuntu/data
fi
echo "Creating /home/ubuntu/data directory..."
sudo mkdir -p /home/ubuntu/data
sudo chown $USER:$USER /home/ubuntu/data

# Setup OpenSora base image
echo "Cloning OpenSora repository..."
if [ -d "Open-Sora" ]; then
    echo "Removing existing Open-Sora directory..."
    rm -rf Open-Sora
fi
git clone $OPEN_SORA_REPO || { echo "Failed to clone OpenSora repository"; exit 1; }
cd Open-Sora
echo "Building OpenSora Docker image..."
sudo docker build -t opensora -f Dockerfile . || { echo "Failed to build OpenSora Docker image"; exit 1; }

# Clone image-eval repository
echo "Cloning image-eval repository..."
cd ~
if [ -d "image-eval" ]; then
    echo "Removing existing image-eval directory..."
    rm -rf image-eval
fi
git clone $IMAGE_EVAL_REPO || { echo "Failed to clone image-eval repository"; exit 1; }


# Build OpenSora inference server image
echo "Building OpenSora inference server Docker image..."
cd image-eval/models/opensora
sudo docker build -t opensora_api . || { echo "Failed to build OpenSora inference server Docker image"; exit 1; }

# Run the inference server
echo "Running OpenSora inference server..."
sudo docker run -d --gpus all -p 5000:5000 -v /home/ubuntu/data:/data opensora_api:latest || { echo "Failed to run OpenSora inference server Docker container"; exit 1; }

echo "Deployment script completed successfully."

# Print example request
echo "You can make a request to the inference server using the following command:"
echo "curl -X POST http://SERVER_IP:5000/generate -H \"Content-Type: application/json\" -d '{
    \"num_frames\": \"24\",
    \"resolution\": \"240p\",
    \"aspect_ratio\": \"16:9\",
    \"prompt\": \"a beautiful sunset\",
    \"save_dir\" : \"/data\"
}' --output /tmp/opensora_sample.mp4"
