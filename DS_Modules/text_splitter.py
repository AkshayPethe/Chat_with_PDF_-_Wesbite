from langchain.text_splitter import RecursiveCharacterTextSplitter


def TextSplitter(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
    
                                                chunk_size=300,
                                                chunk_overlap=30,
                                                length_function=len,
                                                is_separator_regex=False)
        return text_splitter
  
    except Exception as e:
        print(f"Error Occurred while Text Splitting into Chunks: {e}")

    
