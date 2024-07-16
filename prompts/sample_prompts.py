import os
import random

NUM_PROMPTS = 50

def sample_prompts(prompts_file, n_sample):
    # Load prompts from file
    with open(prompts_file, 'r') as file:
        prompts = file.readlines()
    
    # Ensure n_sample does not exceed the number of available prompts
    n_sample = min(n_sample, len(prompts))
    print(n_sample)
    
    # Randomly sample n_sample prompts
    sampled_prompts = random.sample(prompts, n_sample)
    print(len(sampled_prompts))
    
    return [prompt.strip() for prompt in sampled_prompts]

def print_prompts(prompts):
    for p in prompts:
        print(p)

if __name__ == "__main__":

    path = "/home/eole/Workspaces/image-eval/prompts/all_category.txt"
    sampled = sample_prompts(path, 50)

    print(len(sampled))
    print_prompts(sampled)