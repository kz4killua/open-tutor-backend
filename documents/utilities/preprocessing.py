from typing import Iterable
import fitz
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

# To avoid ambiguity, conflicting Document imports are renamed more explicitly
from ..models import Document as OpenTutorDocument
from langchain_core.documents.base import Document as LangChainDocument


def clip_text(text: str, max_tokens: int, model_name: str) -> str:
    """Clip the provided text to the specified number of tokens."""
    enc = tiktoken.encoding_for_model(model_name)
    tokens = enc.encode(text)
    return enc.decode(tokens[:max_tokens])


def extract_text_from_document(document: OpenTutorDocument):
    """Returns texts for each page of an OpenTutor document."""

    # Read the text from each page of the OpenTutorDocument
    with fitz.open(stream=document.file.file.read()) as f:
        pages = {
            int(page_number): page.get_text() for page_number, page in enumerate(f, 1)
        }

    return pages


def chunk_documents(documents: Iterable[LangChainDocument]) -> list[LangChainDocument]:
    """Perform chunking on an array of LangChain Documents."""
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o",
        chunk_size=1024,
        chunk_overlap=128,
    )
    return splitter.split_documents(documents)