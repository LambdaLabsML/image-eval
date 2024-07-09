import os
import streamlit as st
import torch
from huggingface_hub import HfApi, HfFolder
from utils.utils import get_device, generate_image

# Set environment variable to turn off oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Set your Hugging Face token (recommended to set this as an environment variable)
HF_TOKEN = os.getenv('HF_TOKEN')

if HF_TOKEN is None:
    raise ValueError("Hugging Face token is not set. Please set the HF_TOKEN environment variable.")

# Save the Hugging Face token
HfFolder.save_token(HF_TOKEN)
api = HfApi()

# List of diverse prompts
from utils.prompts import get_prompts
prompts = get_prompts()
prompts = prompts[:2]

# List of text-to-image models
# from utils.models import get_models
# models = get_models()
models_debug = ["stabilityai/stable-diffusion-2-1"]
model_1 = st.selectbox("Select the first text-to-image model", models_debug)
model_2 = st.selectbox("Select the second text-to-image model", models_debug)

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

# Initialize session state for storing generated images
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = {}

if st.button("Generate"):
    num_gpus = torch.cuda.device_count()
    gpu_index = 0
    progress_bar = st.progress(0)
    total_steps = len(prompts) * 2  # Total number of images to be generated

    for i, prompt in enumerate(prompts):
        st.session_state.generated_images[prompt] = {}
        device = get_device(gpu_index % num_gpus)
        image_1 = generate_image(model_1, prompt, device)
        progress_bar.progress((i * 2 + 1) / total_steps)
        image_2 = generate_image(model_2, prompt, device)
        progress_bar.progress((i * 2 + 2) / total_steps)
        st.session_state.generated_images[prompt]['image_1'] = image_1
        st.session_state.generated_images[prompt]['image_2'] = image_2
        gpu_index += 2

# Display stored images with checkboxes
for prompt, images in st.session_state.generated_images.items():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='center-vertical'>{prompt}</div>", unsafe_allow_html=True)
    with col2:
        st.image(images['image_1'])
        st.checkbox("Select Image 1", key=f"checkbox_{prompt}_1_persist")
    with col3:
        st.image(images['image_2'])
        st.checkbox("Select Image 2", key=f"checkbox_{prompt}_2_persist")
