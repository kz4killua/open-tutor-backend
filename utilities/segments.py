import re


def clean_extra_whitespace(text: str) -> str:
    """
    Cleans extra whitespace characters that appear between words.

    Credits: https://pypi.org/project/unstructured/
    """
    cleaned_text = re.sub(r"[\xa0\n]", " ", text)
    cleaned_text = re.sub(r"([ ]{2,})", " ", cleaned_text)
    return cleaned_text.strip()


def split_text_into_chunks(text):
    """
    Splits a piece of text into one or more chunks.
    """

    text = clean_extra_whitespace(text)

    # Count the number of chunks to split into
    chunk_size = 1280
    number_of_chunks = min((len(text) // chunk_size), 10)
    number_of_chunks = max(number_of_chunks, 1)

    # Split the text into chunks
    chunks = []
    for i in range(number_of_chunks):
        chunks.append(text[i * (len(text) // number_of_chunks) : (i + 1) * (len(text) // number_of_chunks)])

    return chunks