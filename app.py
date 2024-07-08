import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import ImageOps
import requests
import huggingface_hub

# Function to fetch and filter top trendy text-to-image models
def get_top_trendy_text_to_image_models():

    # Deprecating search of trendy because too many issues (eg: exclude=['stability', 'inpainting'])
    # models = huggingface_hub.list_models(filter="text-to-image", sort="downloads", direction=-1, limit=10)
    # models = [m.id for m in models]
    # models = [model_id for model_id in models if not any(exclude_word in model_id for exclude_word in exclude)]

    models = [
        "stabilityai/stable-diffusion-3-medium",
        "stabilityai/stable-diffusion-3-medium-diffusers",
        "stabilityai/sdxl-turbo",
        "stabilityai/stable-diffusion-xl-base-1.0",
        "Kwai-Kolors/Kolors",
        "mann-e/Mann-E_Dreams",
        "runwayml/stable-diffusion-v1-5",
        "stabilityai/stable-diffusion-2-1",
        "cagliostrolab/animagine-xl-3.1",
        "ByteDance/SDXL-Lightning",
        "ByteDance/Hyper-SD",
    ]
    return models

# Fetch the top trendy models
models = get_top_trendy_text_to_image_models()

if models:
    # Create dropdowns for selecting models
    model_1 = st.selectbox("Select the first text-to-image model", models)
    model_2 = st.selectbox("Select the second text-to-image model", models)
else:
    st.error("No models available to select.")

# List of diverse prompts
prompts = [
    "A futuristic cityscape at sunset with flying cars",
    "A serene beach with crystal clear water and palm trees",
    "A bustling marketplace in an ancient city",
    "A snowy mountain landscape with a cozy cabin",
    "A vibrant underwater scene with colorful coral reefs",
    "A fantasy castle on a floating island",
    "A dense jungle with exotic wildlife",
    "A futuristic robot in a high-tech laboratory",
    "A peaceful countryside with rolling hills and farmhouses",
    "A mysterious cave with glowing crystals",
    "A crowded city street at night with neon lights",
    "A space station orbiting a distant planet"
]

def get_device(index):
    return torch.device(f'cuda:{index}')

@st.cache_resource
def load_model(model_name):
    return StableDiffusionPipeline.from_pretrained(
        model_name, 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True  # Enable low CPU memory usage
    )

def generate_image(model_name, prompt, device):
    pipe = load_model(model_name)
    pipe = pipe.to(device)  # Use specified GPU for inference
    image = pipe(prompt).images[0]
    return image

# CSS to center the prompts vertically
st.markdown(
    """
    <style>
    .center-vertical {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 200px; /* Adjust this height as needed */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button("Generate"):
    num_gpus = torch.cuda.device_count()
    gpu_index = 0

    for prompt in prompts:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='center-vertical'>{prompt}</div>", unsafe_allow_html=True)
        with col2:
            device = get_device(gpu_index % num_gpus)
            image_1 = generate_image(model_1, prompt, device)
            st.image(image_1)
            gpu_index += 1
        with col3:
            device = get_device(gpu_index % num_gpus)
            image_2 = generate_image(model_2, prompt, device)
            st.image(image_2)
            gpu_index += 1
