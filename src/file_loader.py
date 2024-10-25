from langchain_community.document_loaders import PyPDFLoader
from langchain.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.youtube import TranscriptFormat


def get_pdf(file_path):    
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages


def get_youtube(url):
    loader = YoutubeLoader.from_youtube_url(
        url,
        transcript_format=TranscriptFormat.CHUNKS,
        chunk_size_seconds=30)
    return loader.load()


def get_web_content(link):
    loader= WebBaseLoader(link)
    docs = loader.load_and_split()
    return docs