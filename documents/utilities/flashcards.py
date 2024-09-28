import re
from documents.models import Flashcard
from openai import OpenAI

from .preprocessing import clip_text
from .templates import FLASHCARD_CREATE_PROMPT_TEMPLATE


client = OpenAI()


def create_flashcards(document, text):
    """Creates and saves flashcard objects using the given text."""

    model_name = "gpt-4o-mini"
    max_tokens = 127_000
    text = clip_text(text, max_tokens, model_name)

    # Use an LLM to generate the flashcards
    prompt = FLASHCARD_CREATE_PROMPT_TEMPLATE.render(
        text=text
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    response_content = response.choices[0].message.content

    # Parse the LLM response and create the flashcards
    for front, back in parse_llm_response_for_flashcards(response_content):
        Flashcard.objects.create(
            document=document,
            front=front.strip(),
            back=back.strip()
        )


def parse_llm_response_for_flashcards(text):
    """Extracts flashcards from the LLM response."""
    pattern = r"Front: (.+?)\nBack: (.+?)\n"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches