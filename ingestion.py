from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader, PyPDFDirectoryLoader
from constants import CHROMA_SETTINGS

loader = PyPDFDirectoryLoader("./docs/")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
texts = text_splitter.split_documents(documents)

embedding_function = SentenceTransformerEmbeddings(model_name="LaMini-T5-738M")

db = Chroma.from_documents(texts, embedding_function, persist_directory="db", client_settings=CHROMA_SETTINGS)
print("done")