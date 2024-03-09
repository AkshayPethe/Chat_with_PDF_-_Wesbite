import os
import io
import uuid
import base64
from base64 import b64decode
import numpy as np
import time
from PIL import Image
from unstructured.partition.pdf import partition_pdf
from langchain_community.document_loaders import WebBaseLoader #For BeautifulSoup
import requests

from PyPDF2 import PdfReader

def Pdf_Reader(pdf_docs):
    try:
        text = ""
        pdf_file = PdfReader(pdf_docs)
        for page in pdf_file.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error Occurred while extracting text from PDF File: {e}")




def get_text_for_url(website_url):
    try:
        loader = WebBaseLoader(website_url)
        documents = loader.load()
    
    except requests.exceptions.RequestException as e:
        print(f"Error loading URL: {e}")
        return None
    
    return documents
