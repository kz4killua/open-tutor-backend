import re
from documents.models import Flashcard
from openai import OpenAI

from .templates import OVERVIEW_PROMPT_TEMPLATE


client = OpenAI()


def create_overview(text):

    # Use an LLM to generate the overview
    prompt = OVERVIEW_PROMPT_TEMPLATE.render(
        text=text
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    response_content = response.choices[0].message.content

    return response_content