import webbrowser  # Optional
from llmsherpa.readers import LayoutPDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document, VectorStoreIndex

try:


    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
    pdf_url = "https://arxiv.org/pdf/2402.06196.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
    pdf_reader = LayoutPDFReader(llmsherpa_api_url)
    doc = pdf_reader.read_pdf(pdf_url)
    for chunks in doc.chunks():
        print(chunks.to_text())
    
#     document = []
#     for chunks in doc.chunks():
#        m =  Document(text=chunks.to_context_text(), extra_info={})
#        document.append(m)

#     parser = SentenceSplitter()
#     nodes = parser.get_nodes_from_documents(document)

# # build index
#     index = VectorStoreIndex(nodes)

#     print(index)


except Exception as e:
    print(f"An error occurred: {e}")


