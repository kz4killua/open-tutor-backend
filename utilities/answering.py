import os

from openai import OpenAI
from jinja2 import Environment, FileSystemLoader


# Setup OpenAI
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

# Set up Jinja
JINJA_ENV = Environment(loader=FileSystemLoader('./utilities/prompts'))
QUESTION_ANSWERING_TEMPLATE = JINJA_ENV.get_template('question_answering.jinja2')



def generate_response_to_question(question, knowledge):
    """
    Use Azure OpenAI to get an answer to a question.
    """

    # Create a prompt to use
    prompt = QUESTION_ANSWERING_TEMPLATE.render(
        text=knowledge, question=question
    )

    # Generate a response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return completion.choices[0].message.content