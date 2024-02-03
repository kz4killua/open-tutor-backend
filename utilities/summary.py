import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


# Setup the text analysis client
client = TextAnalyticsClient(
    endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"),
    credential=AzureKeyCredential(
        os.getenv("AZURE_LANGUAGE_KEY")
    )
)


def perform_abstractive_summary(documents):
    """
    Summarizes pieces of text using Azure Language Service.
    """
    
    # Perform document summarization
    poller = client.begin_abstract_summary(
        documents=documents
    )
    results = poller.result()

    # Summarize each piece of text
    summaries = []

    for result in results:

        summary = ""
        
        if result.kind == "AbstractiveSummarization":
            for item in result.summaries:
                summary += f"{item.text} "
        
        elif result.is_error:
            continue
        
        summaries.append(summary)
        
    return summaries