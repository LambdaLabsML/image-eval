# Deploying OpenSora 1.2 for inference on Lambda On-demand Cloud instances

## Setup

Build opensora base image
```bash
git clone https://github.com/hpcaitech/Open-Sora.git
cd Open-Sora
sudo docker build -t opensora -f Dockerfile .
```

Clone this repo if you haven't already:
```bash
cd ~
git clone https://github.com/LambdaLabsML/image-eval.git
```

Build opensora inference server image
```bash
cd image-eval/models/opensora
sudo docker build -t opensora_api  .
```

Run the inference server
```bash
sudo docker run -d --gpus all -p 5000:5000 -v /home/ubuntu/data:/data opensora_api:latest
```

To shut down the running container
```bash
sudo docker ps # identify name of container to stop
sudo docker stop <container_name> # stop container
```


## Usage

Make request to the inference server:
```bash
export SERVER_IP=150.136.145.26
curl -X POST http://${SERVER_IP}:5000/generate -H "Content-Type: application/json" -d '{
    "num_frames": "24",
    "resolution": "240p",
    "aspect_ratio": "16:9",
    "prompt": "a beautiful sunset",
    "save_dir" : "/data"
}' --output /tmp/opensora_sample.mp4
```



## Usage (deprecated)

Run container in interactive mode:
```bash
mkdir home/ubuntu/data
sudo docker run -ti --gpus all -v /home/ubuntu/data:/data opensora
```

Run inference in container:
```bash
(pytorch) root@6a7431d9eadb:/workspace/Open-Sora# 
python scripts/inference.py \
    configs/opensora-v1-2/inference/sample.py \
    --num-frames 4s \
    --resolution 360p \
    --aspect-ratio 9:16 \
    --prompt "a beautiful waterfall" \
    --save-dir /data
```




---


Notes:
* source: https://github.com/hpcaitech/Open-Sora?tab=readme-ov-file#inference
* Ran into issues with non docker route stemming from different CUDA version in ODC and in the OpenSora docs. For instance, xformers was not compatible with the CUDA version in the ODC. Tried building from source to no avail.
* Needed to use `sudo` with docker because I ran into permission issue using docker on ODC otherwise