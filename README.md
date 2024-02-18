## Open Tutor
This repository contains the code for the backend of the OpenTutor application. You can check out the frontend [here](https://github.com/kz4killua/opentutor-frontend). 

## What does it do?
Open Tutor analyzes the contents of a textbook, research paper, assignment, or even magazine, and steps the learner through the content. Rather than having to deal with a huge mess of confusing text, Open Tutor breaks down difficult material into simple easy-to-digest modules. After completing each module, you get a chance to test your knowledge with evaluation questions. Plus, you have a personal AI tutor that can answer any questions and guide you along the way. 

## What technologies were used?
The backend application is written in Python (with Django REST framework). It uses an Azure PostgreSQL server, Azure Redis Cache, Azure AI Document Intelligence, Azure Language Service (Document Summarizer), and Azure Open AI. 

## Where can I try it?
[Here!](http://tinyurl.com/open-tutor)

## Can I run Open Tutor on my machine? 
Absolutely! Follow these steps:

1. Make sure Python is installed on your machine. Follow the steps here: https://www.python.org/downloads/
2. Navigate to the project directory in your terminal. 
3. It is recommended to create a virtual environment to run the Django app. To create a virtual environment on Windows, use `python3 -m venv venv`. To start the environment, use `./venv/Scripts/activate`. 
4. Run `python3 -m pip install requirements.txt` to install project dependencies. 
5. Create the `.env` file in the root project directory. Take a look at the `.env.example` file for some guidance.
6. Apply migrations using `python3 manage.py migrate`. 
7. Optionally, create a superuser using `python3 manage.py createsuperuser`. This will allow you to access the admin page, at localhost:8000/admin
6. To start the server, run `python3 manage.py runserver`. This wil start the backend server at localhost:8000
7. You probably want to run the frontend application as well. Head over to the [frontend repository](https://github.com/kz4killua/opentutor-frontend) and follow the steps there too. 

# Can I contribute? 
Yes please! Open Tutor is currently open (pun intended), and we welcome everyone to contribute.
