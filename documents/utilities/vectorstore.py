from django.conf import settings

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from documents.utilities.preprocessing import chunk_documents


embedding = OpenAIEmbeddings(model='text-embedding-3-small')
index_name = settings.PINECONE_INDEX_NAME
vectorstore = PineconeVectorStore(
    index_name=index_name, embedding=embedding
)


def upload_langchain_documents_to_vectorstore(langchain_documents, user_id):
    """Upload a list of langchain documents to the vectorstore."""
    langchain_documents = chunk_documents(langchain_documents)
    pinecone_ids = vectorstore.add_documents(langchain_documents, namespace=str(user_id))
    return pinecone_ids


def retrieve_relevant_documents(query, user_id, document_id):
    """Retrieve the most relevant texts to respond to a query."""
    return vectorstore.similarity_search(query, namespace=str(user_id), filter={
        'document_id': document_id
    })


def delete_vectors_from_vectorstore(vector_ids, user_id):
    return vectorstore.delete(vector_ids, namespace=str(user_id))