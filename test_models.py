import requests

API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers=headers
)

print("Status Code:", response.status_code)

data = response.json()

if "data" in data:

    print("\nSearching for Flux / Stable Diffusion...\n")

    keywords = [
        "flux",
        "stable",
        "stability",
        "diffusion",
        "black",
        "forest",
        "sdxl",
        "image"
    ]

    found = False

    for model in data["data"]:

        model_id = model.get("id", "").lower()

        if any(k in model_id for k in keywords):
            print(model_id)
            found = True

    if not found:
        print(
            "No Flux/Stable Diffusion "
            "models found."
        )

else:
    print(data)