# Deploying OpenSora 1.2 for inference on Lambda On-demand Cloud instances

source: https://github.com/hpcaitech/Open-Sora?tab=readme-ov-file#inference


### Setup

Build opensora base image
```bash
git clone https://github.com/hpcaitech/Open-Sora.git
cd Open-Sora
sudo docker build -t opensora .
```

Build opensora inference server image
```bash
sudo docker build opensora_api -f image_eval/models/opensora/Dockerfile .
```

Run container in interactive mode:
```bash
mkdir home/ubuntu/data
sudo docker run -ti --gpus all -v /home/ubuntu/data:/data opensora
```

Notes:
* Ran into issues with non docker route stemming from different CUDA version in ODC and in the OpenSora docs. For instance, xformers was not compatible with the CUDA version in the ODC. Tried building from source to no avail.
* Needed to use `sudo` with docker because I ran into permission issue using docker on ODC otherwise

### Usage


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

