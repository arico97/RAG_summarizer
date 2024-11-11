from fastapi import APIRouter, HTTPException
from typing import List

from pydantic import BaseModel
from . import RAG


# FastAPI setup
api_router = APIRouter()

class ChatHistoryEntry(BaseModel):
    prompt: str
    answer: str

# Data models for requests and responses
class InitializeRequest(BaseModel):
    documents: str
    source_type: str

class DocumentRequest(BaseModel):
    documents: str
    source_type: str

class QueryRequest(BaseModel):
    query: str
    chat_history: List[ChatHistoryEntry]

class AnswerResponse(BaseModel):
    answer: str

# Initialize the RAG model with dummy values (empty documents and default source type)
@api_router.post("/initialize-rag/")
async def initialize_rag(init_request: InitializeRequest):
    """
    Initializes the RAG model with a document and source type, setting up the FAISS index.
    """
    try:
        global rag_model 
        rag_model = RAG(init_request.documents, init_request.source_type)
        response = "RAG created!"
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@api_router.post("/add-documents/")
async def add_documents(doc_request: DocumentRequest):
    """
    Endpoint to add documents to the RAG model's embedding index.
    This will initialize or update the document embeddings.
    """
    try:
        # Update RAG model embeddings
        response = rag_model.add_documents_to_embedding(
            doc_request.documents,
            doc_request.source_type)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/answer/")
async def answer_query(query_request: QueryRequest):
    """
    Endpoint to query the RAG model.
    This will return a generated answer based on the query and the RAG's embedded knowledge.
    """
    try:
        # Generate an answer for the provided query
        chat_history_tuples = [(entry.prompt, entry.answer) for entry in query_request.chat_history]
        answer = rag_model.invoke_answer(query_request.query,
            chat_history_tuples)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
