import os
from langchain.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
import boto3
from config import FAISS_INDEX_PATH

bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

def vector_store_exists():
    return os.path.exists(FAISS_INDEX_PATH)

def init_vector_store(docs, save=True):
    vector_store = FAISS.from_documents(docs, bedrock_embeddings)
    if save:
        vector_store.save_local(FAISS_INDEX_PATH)
    return vector_store
