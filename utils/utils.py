import torch
from utils.models import load_model

def get_device(index):
    return torch.device(f'cuda:{index}')

def generate_image(model_name, prompt, device):
    pipe = load_model(model_name)
    pipe = pipe.to(device)  # Use specified GPU for inference
    image = pipe(prompt).images[0]
    return image