from typing import Iterable
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter

# To avoid ambiguity, conflicting Document imports are renamed more explicitly
from ..models import Document as OpenTutorDocument
from langchain_core.documents.base import Document as LangChainDocument


def count_tokens(text: str):
    """Estimates the number of tokens in a piece of text."""
    return len(text) // 4


def extract_text_from_document(document: OpenTutorDocument):
    """
    Returns an array of LangChain Documents for each page of an uploaded OpenTutorDocument.
    """

    # Read the text from each page of the OpenTutorDocument
    with fitz.open(stream=document.file.file.read()) as f:
        pages = [page.get_text() for page in f]

    # Convert the texts into LangChain Documents
    pages = [LangChainDocument(page, metadata={
        'document_id': document.id, 'page_number': i
    }) for i, page in enumerate(pages, 1)]

    return pages


def perform_text_splitting(documents: Iterable[LangChainDocument]):
    """
    Perform chunking on an array of LangChain Documents.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=32, length_function=count_tokens
    )
    return splitter.split_documents(documents)