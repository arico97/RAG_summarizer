from langchain_community.document_loaders import YoutubeLoader, PyPDFLoader, WebBaseLoader, UnstructuredEPubLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain.text_splitter import RecursiveCharacterTextSplitter

from typing import List

chunk_size = 256
chunk_overlap = 50

def get_pdf_content(file_path: str) -> List:  
    """Load and split a PDF document into pages.
    Args:
        file_path (str): The path to the PDF file to be loaded.

    Returns:
        List: A list of page contents extracted from the PDF.
    """  
    loader = PyPDFLoader(file_path)
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    pages = loader.load()
    documents=text_splitter.split_documents(pages)
    return documents



def get_youtube_content(url: str) -> List:
    """Load and split a YouTube video transcript into chunks.
    Args:
        url (str): The URL of the YouTube video to be loaded.

    Returns:
        List: A list of transcript chunks, split at 30-second intervals.
    """
    loader = YoutubeLoader.from_youtube_url(
        url,
        transcript_format=TranscriptFormat.CHUNKS,
        add_video_info=False,
        chunk_size_seconds=10)
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    pages = loader.load()
    documents=text_splitter.split_documents(pages)
    return documents


def get_web_content(link: str) -> List:
    """Load and split the content from a web page.

    Args:
        link (str): The URL of the web page to be loaded.

    Returns:
        List: A list of document chunks extracted from the web page.
    """
    loader= WebBaseLoader(link)
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    pages = loader.load()
    documents=text_splitter.split_documents(pages)
    return documents

def get_epub_content(file_path: str) -> List: 
    """Load and split an .epub file into pages.
    Args:
        file_path (str): The path to the .epub file to be loaded.

    Returns:
        List: A list of page contents extracted from the epub.
    """ 
    loader = UnstructuredEPubLoader(file_path)
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    pages = loader.load()
    documents=text_splitter.split_documents(pages)
    return documents