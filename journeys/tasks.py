import io

from celery import shared_task

from utilities.reader import extract_text_from_document
from utilities.summary import perform_abstractive_summary
from utilities.evaluation import generate_evaluation_questions

from django.shortcuts import get_object_or_404

from .models import Journey

from sections.models import Section


@shared_task()
def create_journey_task(journey_id):

    # Retrieve the journey
    journey = get_object_or_404(Journey, id=journey_id)

    # Retrieve the uploaded file
    base_file = io.BytesIO(journey.base_file.file.read())
    
    # Extract the text content of the uploaded file
    sections = extract_text_from_document(base_file)

    # Generate a summary for each section
    summaries = perform_abstractive_summary(sections)

    # Generate questions and answers for the section
    evaluations = [
        generate_evaluation_questions(text) for text in summaries
    ]

    for summary, evaluation in zip(summaries, evaluations):
        Section.objects.create(
            journey=journey,
            content=summary,
            evaluation=evaluation
        )