from openai import OpenAI
from config import OPENROUTER_API_KEY
from prompts import SYSTEM_PROMPT

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def generate_news_prompt(news_text):
    print("USING MODEL:", 
              "openai/gpt-3.5-turbo")
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
                News:

                {news_text}

                Create the best editorial image prompt.
                """
            }
        ]
    )

    return response.choices[0].message.content.strip()