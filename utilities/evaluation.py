import os

import openai
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader


# Setup OpenAI
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

# Set up Jinja
JINJA_ENV = Environment(loader=FileSystemLoader('./utilities/prompts'))
MULTIPLE_CHOICE_QUESTIONS_TEMPLATE = JINJA_ENV.get_template('multiple_choice_questions.jinja2')



def generate_evaluation_questions(text):
    """
    Generate evaluation questions for a piece of text using Azure OpenAI.
    """

    # Create a prompt to use
    prompt = MULTIPLE_CHOICE_QUESTIONS_TEMPLATE.render(
        text=text
    )

    # Generate a response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message.content