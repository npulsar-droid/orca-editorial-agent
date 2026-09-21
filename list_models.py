import os
from openai import OpenAI
with open("/Users/pulsar/Downloads/orcarouter-1.txt", "r") as f:
    key = f.read().strip()
client = OpenAI(base_url="https://api.orcarouter.ai/v1", api_key=key) # guessing endpoint from main.py
models = client.models.list()
for m in models.data:
    print(m.id)
