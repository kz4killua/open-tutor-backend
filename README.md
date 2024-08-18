# ✨ Open Tutor: Everything you need to study with AI
Open Tutor aims to be a one-stop shop for AI-powered study tools. This was originally a [hackathon](https://devpost.com/software/open-tutor-vg7s0u) project, but I have decided to take this a bit further. The goal is to make something I would actually use, and not just a gimmick. 

> [!NOTE]
> This repository contains code for the **backend** of the Open Tutor application. You can check out the backend [here](https://github.com/kz4killua/open-tutor-frontend).

## What can it do? 
A lot! Here are some of our features: 

- **AI assistance whenever you need it**: Get explanations, answers to questions, and much more with our powerful AI tutor. The AI tutor is built on GPT 4o, the latest in OpenAI's suite of large language models.
- **Intelligent flashcards that get you**: Create flashcards at the click of a button. Flashcards can adjust to help you focus on your weaknesses.
- **Detailed progress reports**: Get detailed feedback on your performance as well as suggested study areas.
- *more coming soon...*

## Where can I try it? 
[Here!](https://opentutor.ifeanyiobinelo.com/)

## Can I run Open Tutor on my machine?
Absolutely! Follow these steps:

1. Make sure the following are installed:
   - Docker
   - Docker Compose
2. Navigate to the project directory in your terminal.
3. Set up a *.env* file in the root directory for this project. Refer to *.env.example* for more details.
4. Build the Docker image: `docker-compose build`
5. Start the application: `docker-compose up`
6. The application should now be running. Access it through your web browser at localhost:8000.
7. You probably want to run the frontend application as well. Head over to the [frontend repository](https://github.com/kz4killua/open-tutor-frontend) and follow the steps there too. 

## Can I contribute? 
Yes please! Open Tutor is currently open (pun intended), and we welcome everyone to contribute.
