import json
from documents.models import Message, Document
from documents.utilities.vectorstore import retrieve_relevant_documents
from django.shortcuts import get_object_or_404
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI


JINJA_ENV = Environment(loader=FileSystemLoader('./documents/prompts'))
USER_MESSAGE_PROMPT_TEMPLATE = JINJA_ENV.get_template('user_message.jinja2')
SYSTEM_MESSAGE_PROMPT_TEMPLATE = JINJA_ENV.get_template('system_message.jinja2')

client = OpenAI()


def construct_user_message(document, query, quote=None):
    return Message(
        document=document,
        role="user",
        content=query,
        quote=quote
    )


def construct_system_message(user_message):
    
    sources = retrieve_relevant_documents(
        query=f"{user_message.content}\n\n{user_message.quote}",
        user_id=user_message.document.user.id,
        document_id=user_message.document.id
    )
    context = "\n".join([
        item.page_content for item in sources
    ])

    return Message(
        document=user_message.document,
        role="system",
        content=SYSTEM_MESSAGE_PROMPT_TEMPLATE.render(
            context=context,
        ),
        quote=None
    )


def construct_assistant_message(user_message):
    return Message(
        document=user_message.document,
        role="assistant",
        content="",
        quote=None
    )


def create_openai_message(message: Message):
    """
    Format a message for use with OpenAI's API.
    """

    if message.role == "user":
        content = USER_MESSAGE_PROMPT_TEMPLATE.render(
            query=message.content, quote=message.quote
        )
    else:
        content = message.content

    return {
        "role": message.role,
        "content": content
    }


def stream_message_response(user_message, system_message, assistant_message, message_history):
    
    messages = list(map(create_openai_message, [
        system_message, *reversed(message_history), user_message
    ]))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    # Commit messages to the database and generate IDs
    user_message.save()
    system_message.save()
    assistant_message.save()

    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta.content:
            token = delta.content
            assistant_message.content += token

            # Stream responses as data-only SSEs
            event = json.dumps({
                "token": token,
                "assistant_message_id": assistant_message.id,
                "user_message_id": user_message.id
            })
            yield f"\ndata: {event}\n\n"

    # Save changes to the assistant message
    assistant_message.save()