import re
from documents.models import Flashcard
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI


JINJA_ENV = Environment(loader=FileSystemLoader('./documents/prompts'))
FEEDBACK_PROMPT_TEMPLATE = JINJA_ENV.get_template('feedback.jinja2')

client = OpenAI()


def get_feedback(questions_correct, questions_wrong):
    """Generates feedback for a set of questions."""
    
    # Use an LLM to generate the feedback
    prompt = FEEDBACK_PROMPT_TEMPLATE.render(
        questions_correct=questions_correct,
        questions_wrong=questions_wrong
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    response_content = response.choices[0].message.content

    # Parse the LLM response
    feedback = [
        line.strip().removeprefix('- ') 
            for line in response_content.splitlines()
    ]
    feedback = [
        item for item in feedback if item
    ]

    return feedback