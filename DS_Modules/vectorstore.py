from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import chroma

from DS_Modules.pdf_reader import Pdf_Reader
from DS_Modules.websiteparse import  get_text_for_url
from DS_Modules.text_splitter import TextSplitter


def vectorstore_pdf(pdf_docs):
    try:
    
        text = Pdf_Reader(pdf_docs)
        text_chunks= TextSplitter(text)
        vector_store = chroma(text_chunks,OpenAIEmbeddings())

        return vector_store
    except Exception as e:
        print(f"Error Occurred while VectorStoring PDF File: {e}")


def vectorstore_url(url):
    try:
    
        documents = get_text_for_url(website_url)
        text_chunks= TextSplitter(text)
        vector_store = chroma(text_chunks,OpenAIEmbeddings())

        return vector_store
    except Exception as e:
            print(f"Error Occurred while VectorStoring Wesbite content: {e}")

