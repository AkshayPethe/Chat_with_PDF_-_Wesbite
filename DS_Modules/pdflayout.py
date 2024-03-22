import webbrowser
from llmsherpa.readers import LayoutPDFReader

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_url = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\2307.06435.pdf"
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)

def get_section_text(doc, section_title):
    selected_section = None
    for section in doc.sections():
        if section.title == section_title:
            selected_section = section
            break
    if not selected_section:
        return f"No section titled '{section_title}' found."
    return selected_section.to_html(include_children=True, recurse=True)

def display_table(doc, index):
    tables = doc.tables()
    if index < 0 or index >= len(tables):
        return "Table index out of range."
    return tables[index].to_html()

section_text = get_section_text(doc, '3.4 Human annotation collection')
with open("section_text.html", "w") as f:
    f.write(section_text)
webbrowser.open("section_text.html")

table_html = display_table(doc, 4)
with open("table.html", "w") as f:
    f.write(table_html)
webbrowser.open("table.html")




# print(doc.tables()[5])
# print("#"*100)
# with open("table.html", "w") as f:
#     f.write(table_html)[5]
# webbrowser.open("table.html")

# table_html = doc.tables()[1].to_html()

# # Write HTML content to a file
# with open("table.html", "w") as f:
#     f.write(table_html)

# # Open HTML file in default web browser
# webbrowser.open("table.html")

print("#"*100)
for chunk in doc.chunks():
    print(chunk.to_text())
    print("*"*100)
