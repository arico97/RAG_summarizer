from .file_loader import *
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from uuid import uuid4

to_load = {
    'PDF': get_pdf,
    "PDF_on_web":get_pdf,
    'YouTube': get_youtube,
    'Web': get_web_content
}

load_dotenv()
llm = ChatGroq(
    api_key=os.getenv('GROQ_KEY'),
    model_name='llama3-8b-8192'
    )

prompt_init = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer. 
I will tip you $200 if the user finds the answer helpful. 
<context>
{context}
</context>

Question: {input}""")

class RAG:
    def __init__(self, document, source):
        self.embedding_db = self.get_embeddings(document, source)
        self.retriever = self.embedding_db.as_retriever()
        self.document_chain = create_stuff_documents_chain(llm, prompt_init)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)

    
    def get_initial_docs(self, document, source):
        loader = to_load[source]
        docs = loader(document)
        return docs

    def get_embeddings(self, document, source):
        chunks = self.get_initial_docs(document, source)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        vector_embeddings = FAISS.from_documents(documents=chunks,embedding= embeddings)
        return vector_embeddings

    def add_documents_to_embedding(self, document, source):
        loader = to_load[source]
        docs = loader(document)
        uuids = [str(uuid4()) for _ in range(len(docs))]
        self.embedding_db.add_documents(documents=docs, ids=uuids)

    def qa(self, my_prompt):
        response = self.retrieval_chain.invoke({"input":my_prompt})
        return response['answer']
