from langchain_community.document_loaders import YoutubeLoader, PyPDFLoader, WebBaseLoader, UnstructuredEPubLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

from typing import List

def get_pdf_content(file_path: str) -> List:  
    """Load and split a PDF document into pages.
    Args:
        file_path (str): The path to the PDF file to be loaded.

    Returns:
        List: A list of page contents extracted from the PDF.
    """  
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages


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
        chunk_size_seconds=30)
    return loader.load()


def get_web_content(link: str) -> List:
    """Load and split the content from a web page.

    Args:
        link (str): The URL of the web page to be loaded.

    Returns:
        List: A list of document chunks extracted from the web page.
    """
    loader= WebBaseLoader(link)
    docs = loader.load_and_split()
    return docs

def get_epub_content(file_path: str) -> List: 
    """Load and split an .epub file into pages.
    Args:
        file_path (str): The path to the .epub file to be loaded.

    Returns:
        List: A list of page contents extracted from the epub.
    """ 
    loader = UnstructuredEPubLoader(file_path)
    docs = loader.load_and_split()
    return docs