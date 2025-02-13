'''RAG class to manage document retrieval and generation.'''

from .constants import *

from langchain_community.vectorstores import FAISS

from langchain_core.messages import HumanMessage

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from uuid import uuid4

import logging

from typing import List, Tuple


logging.basicConfig(level=logging.INFO) 



class RAG:
    """Manage document retrieval and generation using embeddings, retrievers, and document chains.
   
     Attributes:
        embedding_db: Embedding database created from the initial document embeddings.
        retriever: Retriever instance created from the embedding database.
        document_chain: Document chain used for generating responses.
        retrieval_chain: Chain that combines retrieval with document generation.
    """

    def __init__(self, document: str, source: str) -> None:
        """Initialize RAG class by setting up embeddings, retrievers, and document/retrieval chains.
        Args:
            document (str): Initial document used to create embeddings.
            source (str): Source identifier for loading documents.
        """
        self.embedding_db = self.get_embeddings(document, source)
        self.retriever = self.embedding_db.as_retriever()
        self.document_chain = create_stuff_documents_chain(llm, prompt_init)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)

    
    def get_initial_docs(self, document: str, source: str) -> List:
        """Load initial documents based on the specified source.
        Args:
            document (str): Document text to load.
            source (str): Source identifier that determines how document is loaded.
        Returns:
            List[str]: List of doc chunks or empty string if default loader is used.
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
            document (str): Document text to embed.
            source (str): Source identifier for loading the document.
        Returns:
            FAISS: FAISS vector store containing the document embeddings.
        """
        chunks = self.get_initial_docs(document, source)
        embeddings = embedding_model
        vector_embeddings = FAISS.from_documents(documents=chunks,
                                                 embedding= embeddings)
        return vector_embeddings

    def add_documents_to_embedding(self, document: str, source: str) -> None:
        """Add new documents to the existing embedding database.
        Args:
            document (str): Document text to embed and add.
            source (str): Source identifier for loading the document.
        """
        loader = to_load[source]
        docs = loader(document)
        uuids = [str(uuid4()) for _ in range(len(docs))]
        self.embedding_db.add_documents(documents=docs, ids=uuids)

    def invoke_answer(self, my_prompt: str, chat_history: List[Tuple[str,str]]) -> str:
        """Generate an answer based on prompt and chat history.
        Args:
            my_prompt (str): User input prompt.
            chat_history (Tuple[str, str]): Tuple of chat history with each entry containing user and bot messages.
        Returns:
            str: Generated answer from the retrieval chain.
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
    