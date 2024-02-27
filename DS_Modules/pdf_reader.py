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
