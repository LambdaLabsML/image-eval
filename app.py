import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# List of available text-to-image models
models = ["CompVis/stable-diffusion-v1-4", "runwayml/stable-diffusion-v1-5"]

# Create dropdowns for selecting models
model_1 = st.selectbox("Select the first text-to-image model", models)
model_2 = st.selectbox("Select the second text-to-image model", models)

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

def generate_image(model_name, prompt):
    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Use GPU for faster inference
    image = pipe(prompt).images[0]
    return image

if st.button("Generate"):
    for prompt in prompts:
        st.write(f"{prompt}")
        col1, col2 = st.columns(2)
        with col1:
            image_1 = generate_image(model_1, prompt)
            st.image(image_1)
        with col2:
            image_2 = generate_image(model_2, prompt)
            st.image(image_2)
