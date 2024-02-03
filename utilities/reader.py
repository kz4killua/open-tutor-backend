import os

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Set up the Azure document analysis client
client = DocumentAnalysisClient(
    endpoint=os.getenv('AZURE_DOCUMENT_READER_ENDPOINT'), 
    credential=AzureKeyCredential(os.getenv('AZURE_DOCUMENT_READER_KEY'))
)

def extract_text_from_document(file):
    """
    Extracts text from an IO file using Azure AI Document Intelligence.

    Supported formats: pdf, jpeg, png, bmp, tiff, heif, docx, xlsx, pptx, html
    """

    poller = client.begin_analyze_document("prebuilt-read", file)
    result = poller.result()

    # Extract the paragraphs from the text
    paragraphs = [paragraph.content for paragraph in result.paragraphs]
    
    return paragraphs