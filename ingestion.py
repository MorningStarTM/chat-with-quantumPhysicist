from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
from constants import CHROMA_SETTINGS

persist_directory = './db'
docs_path = "./docs"

def main():
    for files in os.listdir(docs_path):
        if files.endswith(".pdf"):
            print(files)
            loader = PyPDFLoader(os.path.join(docs_path, files))
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma.from_documents(texts, embedding_function, persist_directory="./db/", client_settings=CHROMA_SETTINGS)
    db.persist()
    db = None

main()
print("done")