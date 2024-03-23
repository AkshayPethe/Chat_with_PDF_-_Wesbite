from llmsherpa.readers import LayoutPDFReader
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def extract_text_llmsherpa(pdf_url):
    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
    pdf_reader = LayoutPDFReader(llmsherpa_api_url)
    doc = pdf_reader.read_pdf(pdf_url)
    text_per_page = {}

    for page_num, page in enumerate(doc.get_pages()):
        page_text = [chunk.to_text() for chunk in page.chunks()]
        text_per_page[page_num] = {"page_text": page_text}
    
    return text_per_page

def extract_tables(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    tables = table_page.extract_tables()
    table = tables[table_num]
    return table

def table_converter(table):
    table_string = ''
    for row_num, row in enumerate(table):
        processed_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string += ('|' + '|'.join(processed_row) + '|' + '\n')
    table_string = table_string[:-1]  # Remove the last newline character
    return table_string

def convert_to_image(input_file):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_Image.png"
    image.save(output_file,"PNG")

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = element.x0, element.y0, element.x1, element.y1
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writter = PyPDF2.PdfWriter()
    cropped_pdf_writter.add_page(pageObj)
    with open('cropped_image.pdf','wb') as cropped_pdf_file:
        cropped_pdf_writter.write(cropped_pdf_file)

def final_extraction(pdf_url):
    text_per_page = extract_text_llmsherpa(pdf_url)
    pdf_path = "temp.pdf"
    pdf_file = open(pdf_path, 'wb')
    for page in extract_pages(pdf_url):
        pdf_file.write(page.encode('utf-8'))
    pdf_file.close()
    
    for page_num, page in enumerate(extract_pages(pdf_path)):
        page_text = [chunk.to_text() for chunk in page.chunks()]
        text_per_page[page_num]["page_text"] += page_text
        
        text_from_image, text_from_tables = [], []
        pdf = pdfplumber.open(pdf_path)
        page_tables = pdf.pages[page_num]
        tables = page_tables.find_tables()
        for i, component in enumerate(page._objs):
            if isinstance(component, LTFigure):
                crop_image(component, page)
                convert_to_image('cropped_image.pdf')
                image_text = image_to_text("PDF_Image.png")
                text_from_image.append(image_text)
            elif isinstance(component, LTRect):
                table = extract_tables(pdf_path, page_num, i)
                table_string = table_converter(table)
                text_from_tables.append(table_string)
        text_per_page[page_num]["text_from_image"] = text_from_image
        text_per_page[page_num]["text_from_tables"] = text_from_tables
    
    return text_per_page

# Example usage:
pdf_url = r"https://arxiv.org/pdf/2401.05618.pdf"
extracted_data = final_extraction(pdf_url)
print("*"*100)
print(extracted_data[1]["page_text"])
