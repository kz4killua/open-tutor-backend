from django.conf import settings

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from documents.utilities.preprocessing import extract_text_from_document, perform_text_splitting


embedding = OpenAIEmbeddings(model='text-embedding-ada-002')
index_name = settings.PINECONE_INDEX_NAME
vectorstore = PineconeVectorStore(
    index_name=index_name, embedding=embedding
)


def upload_open_tutor_document_to_vectorstore(document):
    """
    Extract text from an Open Tutor document and upload to the vectorstore.
    """
    langchain_documents = extract_text_from_document(document)
    langchain_documents = perform_text_splitting(langchain_documents)
    return vectorstore.add_documents(langchain_documents, namespace=str(document.user.id))


def retrieve_relevant_documents(query, user_id, document_id):
    """
    Retrieve the most relevant texts to respond to a query.
    """
    return vectorstore.similarity_search(query, namespace=str(user_id), filter={
        'document_id': document_id
    })


def delete_vectors_from_vectorstore(vector_ids, user_id):
    return vectorstore.delete(vector_ids, namespace=str(user_id))