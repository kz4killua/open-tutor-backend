import re
from documents.models import Flashcard
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI


JINJA_ENV = Environment(loader=FileSystemLoader('./documents/prompts'))
FLASHCARD_CREATE_PROMPT_TEMPLATE = JINJA_ENV.get_template('flashcard_create.jinja2')

client = OpenAI()


def create_flashcards(document, text):
    """Creates and saves flashcard objects using the given text."""

    # Use an LLM to generate the flashcards
    prompt = FLASHCARD_CREATE_PROMPT_TEMPLATE.render(
        text=text
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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