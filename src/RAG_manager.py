from .file_loader import *

from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os 

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.messages import HumanMessage

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from uuid import uuid4

import logging

from typing import List, Tuple


logging.basicConfig(level=logging.INFO) 

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

class RAG:
    """Manage document retrieval and generation using embeddings, retrievers, and document chains.
   
     Attributes:
        embedding_db: The embedding database created from the initial document embeddings.
        retriever: A retriever instance created from the embedding database.
        document_chain: A document chain used for generating responses.
        retrieval_chain: A chain that combines retrieval with document generation.
    """

    def __init__(self, document: str, source: str) -> None:
        """Initialize RAG class by setting up embeddings, retrievers, and document/retrieval chains.
        Args:
            document (str): The initial document used to create embeddings.
            source (str): The source identifier for loading documents.
        """
        self.embedding_db = self.get_embeddings(document, source)
        self.retriever = self.embedding_db.as_retriever()
        self.document_chain = create_stuff_documents_chain(llm, prompt_init)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)

    
    def get_initial_docs(self, document: str, source: str) -> List:
        """Load initial documents based on the specified source.
        Args:
            document (str): The document text to load.
            source (str): The source identifier that determines how the document is loaded.
        Returns:
            List[str]: A list of document chunks or an empty string if the default loader is used.
        """
        loader = to_load[source]
        if loader == 'default':
            docs = ""
        else:
            docs = loader(document)
            logging.info(f"The length of docs is: {len(docs)}")
        return docs

    def get_embeddings(self, document: str, source: str) -> FAISS:
        """Create vector embeddings for the given document.
        Args:
            document (str): The document text to embed.
            source (str): The source identifier for loading the document.
        Returns:
            FAISS: A FAISS vector store containing the document embeddings.
        """
        chunks = self.get_initial_docs(document, source)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        vector_embeddings = FAISS.from_documents(documents=chunks,embedding= embeddings)
        return vector_embeddings

    def add_documents_to_embedding(self, document: str, source: str) -> None:
        """Add new documents to the existing embedding database.
        Args:
            document (str): The document text to embed and add.
            source (str): The source identifier for loading the document.
        """
        loader = to_load[source]
        docs = loader(document)
        uuids = [str(uuid4()) for _ in range(len(docs))]
        self.embedding_db.add_documents(documents=docs, ids=uuids)

    def invoke_answer(self, my_prompt: str, chat_history: List[Tuple[str,str]]) -> str:
        """Generate an answer based on the prompt and chat history.
        Args:
            my_prompt (str): The input prompt from the user.
            chat_history (Tuple[str, str]): A tuple of chat history with each entry containing user and bot messages.
        Returns:
            str: The generated answer from the retrieval chain.
        """
        chat_history_proc =[(HumanMessage(i),j) for i,j in chat_history]
        history = [*sum(chat_history_proc, ())]
        response = self.retrieval_chain.invoke(
            {
                "input":my_prompt,
                "chat_history":history
            }
        )
        answer = response['answer']
        logging.info(answer)
        return answer
    