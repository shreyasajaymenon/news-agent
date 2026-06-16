import os
import base64
import requests

from config import (
    OPENROUTER_API_KEY,
    HUGGINGFACE_API_KEY
)

SAVE_DIR = "generated_images"

os.makedirs(SAVE_DIR, exist_ok=True)


def save_image(
    image_bytes,
    model_name,
    article_num
):
    filename = (
        f"article_{article_num}_"
        f"{model_name}.png"
    )

    filepath = os.path.join(
        SAVE_DIR,
        filename
    )

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    print(f"Saved: {filename}")


def generate_gpt_image(
    prompt,
    article_num
):

    url = (
        "https://openrouter.ai/"
        "api/v1/chat/completions"
    )

    headers = {
        "Authorization":
        f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":
        "application/json"
    }

    payload = {
        "model": "openai/gpt-5-image",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    data = response.json()

    try:
        image_b64 = (
            data["choices"][0]
            ["message"]
            ["images"][0]
            ["image_base64"]
        )

        image_bytes = (
            base64.b64decode(
                image_b64
            )
        )

        save_image(
            image_bytes,
            "gpt",
            article_num
        )

    except Exception:
        print("GPT failed")
        print(data)


def generate_hf_image(
    prompt,
    model_id,
    model_name,
    article_num
):

    API_URL = (
        f"https://api-inference."
        f"huggingface.co/models/"
        f"{model_id}"
    )

    headers = {
        "Authorization":
        f"Bearer "
        f"{HUGGINGFACE_API_KEY}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt
        }
    )

    if response.status_code == 200:

        save_image(
            response.content,
            model_name,
            article_num
        )

    else:
        print(
            f"{model_name} failed:"
        )
        print(response.text)


def generate_image(
    prompt,
    model,
    model_name,
    article_num
):

    if model_name == "gpt":

        generate_gpt_image(
            prompt,
            article_num
        )

    elif model_name == "flux":

        generate_hf_image(
            prompt,
            "black-forest-labs/FLUX.1-schnell",
            "flux",
            article_num
        )

    elif model_name == "sdxl":

        generate_hf_image(
            prompt,
            "stabilityai/"
            "stable-diffusion-xl"
            "-base-1.0",
            "sdxl",
            article_num
        )