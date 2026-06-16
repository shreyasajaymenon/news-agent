from openai import OpenAI
from config import OPENROUTER_API_KEY
from prompts import CRITIC_PROMPT

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def improve_prompt(prompt):

    print(
        "CRITIC MODEL:",
        "openai/gpt-3.5-turbo"
    )

    try:
        response = (
            client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": CRITIC_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    except Exception as e:

        print(
            "Critic agent failed:"
        )
        print(e)

        print(
            "Using original prompt..."
        )

        return prompt