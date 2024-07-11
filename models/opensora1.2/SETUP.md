# Deploying OpenSora 1.2 for inference on Lambda On-demand Cloud instances

source: https://github.com/hpcaitech/Open-Sora?tab=readme-ov-file#inference


### Setup

Installation:
```bash
git clone https://github.com/hpcaitech/Open-Sora.git
cd Open-Sora
sudo docker build -t opensora .
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


---


Requirement: have created a sample config file in shared dir of host.

``/home/ubuntu/data/sample.py`
```python
num_frames = 16
frame_interval = 3
fps = 24
image_size = (240, 426)
multi_resolution = "STDiT2"

# Define model
model = dict(
    type="STDiT2-XL/2",
    from_pretrained="hpcai-tech/OpenSora-STDiT-v2-stage3",
    input_sq_size=512,
    qk_norm=True,
    qk_norm_legacy=True,
    enable_flash_attn=True,
    enable_layernorm_kernel=True,
)
vae = dict(
    type="VideoAutoencoderKL",
    from_pretrained="stabilityai/sd-vae-ft-ema",
    cache_dir=None,  # "/mnt/hdd/cached_models",
    micro_batch_size=4,
)
text_encoder = dict(
    type="t5",
    from_pretrained="DeepFloyd/t5-v1_1-xxl",
    cache_dir=None,  # "/mnt/hdd/cached_models",
    model_max_length=200,
)
scheduler = dict(
    type="iddpm",
    num_sampling_steps=100,
    cfg_scale=7.0,
    cfg_channel=3,  # or None
)
dtype = "bf16"

# Condition
prompt_path = "./assets/texts/t2v_samples.txt"
prompt = "A beautiful sunset over the city"  # prompt has higher priority than prompt_path

# Others
batch_size = 1
seed = 42
save_dir = "/data"
```
