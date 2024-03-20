from llmsherpa.readers import LayoutPDFReader
from IPython.display import display, HTML

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_url = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\ast_sci_data_tables_sample.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)
type(doc)

for chunk in doc.chunks():
    print(chunk.to_text())