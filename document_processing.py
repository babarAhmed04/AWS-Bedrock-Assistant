from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)

def load_and_split_documents(data_dir):
    loader = PyPDFDirectoryLoader(data_dir)
    documents = loader.load()
    return text_splitter.split_documents(documents)
