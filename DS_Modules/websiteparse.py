from langchain_community.document_loaders import WebBaseLoader #For BeautifulSoup

import requests

def get_text_for_url(website_url):
    try:
        loader = WebBaseLoader(website_url)
        documents = loader.load()
    
    except requests.exceptions.RequestException as e:
        print(f"Error loading URL: {e}")
        return None
    
    return documents


