'''Constants for the project'''

from dotenv import load_dotenv
import os 

from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from .file_loader import *

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



to_load = {
    'pdf': get_pdf_content,
    "PDF from web":get_pdf_content,
    'YouTube': get_youtube_content,
    'Web': get_web_content,
    'epub':get_epub_content
}

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv('GROQ_KEY'),
    model_name='llama-3.2-90b-vision-preview'
   # model_name='llama3-8b-8192'
    )

prompt_qa = """
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer. 
I will tip you $200 if the user finds the answer helpful. 
{context}"""

prompt_init = ChatPromptTemplate.from_messages(    
    [
        ("system", prompt_qa),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
            )