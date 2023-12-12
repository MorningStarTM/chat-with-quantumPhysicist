from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import torch
import base64
import textwrap
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from constants import CHROMA_SETTINGS

check_point = "LaMini-T5-738M"

tokenizer = AutoTokenizer.from_pretrained(check_point)
model = AutoModelForSeq2SeqLM.from_pretrained(check_point, device_map="auto", torch_dtype=torch.float32)

def llm_pipeline():
    pipe = pipeline(
        'text2text-generation',
        model = model,
        tokenizer = tokenizer,
        max_length = 256,
        do_sample = True,
        temperature = 0.3,
        top_p = 0.95
    )
    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm

def qa_llm():
    llm = llm_pipeline()
    embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
    db = Chroma(persist_directory='db', embedding_function=embeddings,client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa

def process_answer(instruction):
    response = ''
    instruction = instruction
    qa = qa_llm()
    generated_text = qa(instruction)
    answer = generated_text['result']
    return answer, generated_text

