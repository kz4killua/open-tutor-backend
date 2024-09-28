from openai import OpenAI

from .preprocessing import clip_text
from .templates import OVERVIEW_PROMPT_TEMPLATE


client = OpenAI()


def create_overview(text):

    model_name = "gpt-4o-mini"
    max_tokens = 127_000
    text = clip_text(text, max_tokens, model_name)

    # Use an LLM to generate the overview
    prompt = OVERVIEW_PROMPT_TEMPLATE.render(
        text=text
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    response_content = response.choices[0].message.content

    return response_content