import logging
# Load model directly
from transformers import AutoProcessor, MusicgenForConditionalGeneration, AutoModel
import torch
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small",cache_dir="./model").to(device)
sampling_rate = model.config.audio_encoder.sampling_rate
model.save_pretrained("./model")
print(1)
