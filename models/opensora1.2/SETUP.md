# Deploying OpenSora 1.2 for inference on Lambda On-demand Cloud instances

source: https://github.com/hpcaitech/Open-Sora?tab=readme-ov-file#inference


### Setup

Installation:
```bash
git clone https://github.com/hpcaitech/Open-Sora.git
cd Open-Sora
sudo docker build -t opensora:1.2 .
```

Run container in interactive mode:
```bash
MOUNT_DIR=mnt_dir
sudo docker run -ti --gpus all -v ${MOUNT_DIR}:/data opensora:1.2
```

Notes:
* Ran into issues with non docker route stemming from different CUDA version in ODC and in the OpenSora docs. For instance, xformers was not compatible with the CUDA version in the ODC. Tried building from source to no avail.
* Needed to use `sudo` with docker because I ran into permission issue using docker on ODC otherwise

### Usage

```
# text to video
python scripts/inference.py configs/opensora-v1-2/inference/sample.py \
  --num-frames 4s --resolution 720p --aspect-ratio 9:16 \
  --prompt "a beautiful waterfall"
```