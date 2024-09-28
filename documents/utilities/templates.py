from jinja2 import Environment, FileSystemLoader


JINJA_ENV = Environment(loader=FileSystemLoader('./documents/prompts'))
FEEDBACK_PROMPT_TEMPLATE = JINJA_ENV.get_template('feedback.jinja2')
FLASHCARD_CREATE_PROMPT_TEMPLATE = JINJA_ENV.get_template('flashcard_create.jinja2')
USER_MESSAGE_PROMPT_TEMPLATE = JINJA_ENV.get_template('user_message.jinja2')
SYSTEM_MESSAGE_PROMPT_TEMPLATE = JINJA_ENV.get_template('system_message.jinja2')
OVERVIEW_PROMPT_TEMPLATE = JINJA_ENV.get_template('overview.jinja2')