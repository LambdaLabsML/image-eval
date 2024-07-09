import streamlit as st
from diffusers import StableDiffusionPipeline, StableDiffusion3Pipeline, AutoPipelineForText2Image


def get_models():

    return [
    "stabilityai/stable-diffusion-3-medium-diffusers",
    "runwayml/stable-diffusion-v1-5",
    "stabilityai/stable-diffusion-2-1",
]

@st.cache_resource
def load_model(model_name):

    print(f"[ ] Loading model {model_name}")
    if model_name in ["stabilityai/stable-diffusion-3-medium-diffusers"]:
        pipe = StableDiffusion3Pipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        
    elif model_name in ["stabilityai/sdxl-turbo"]:
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            variant="fp16")
    else:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_name, 
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True  # Enable low CPU memory usage
        )
    print(f"[+] Loaded model {model_name}")
    return pipe