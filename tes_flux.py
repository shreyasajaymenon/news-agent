import os
import replicate
from dotenv import load_dotenv

load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = os.getenv(
    "REPLICATE_API_TOKEN"
)

prompt = """
Editorial news image of Nvidia
announcing next-generation AI chips,
modern tech conference,
realistic newsroom aesthetic,
cinematic lighting
"""

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": prompt
    }
)

print(output)