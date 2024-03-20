# To read the PDF
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber
# To extract the images from the PDFs
from PIL import Image
from pdf2image import convert_from_path
# To perform OCR to extract text from images 
import pytesseract 

import os

"""https://towardsdatascience.com/extracting-text-from-pdf-files-with-python-a-comprehensive-guide-9fc4003d517"""

# Function to Extract Text
def text_extract(element):

    """Extracts text from the corpus, Checking if text is in LTTextContainer and LTChar.If yes extracting format for line

     Args:
      element: The element from which to extract text and line formats.

    Returns:
      A tuple containing (extracted text, list of unique line formats). """

    line_text = element.get_text() #Method of LTTEContrainer which extract words within the corpus box and store in a list
    line_format = []  
    for text_line in element:
        if isinstance(text_line,LTTextContainer):
            line_format = [(char.fontname,char.size) for char in text_line if isinstance(char,LTChar)]
    format_per_line = list(set(line_format))
    return (line_text, format_per_line)




#For Image Extraction and Text from Images
def crop_image(element,pageObj):
    """We use the metadata from the LTFigure object detected from PDFMiner to 
    crop the image box, utilising its coordinates in the page layout. 
    We then save it as a new PDF in our directory using the PyPDF2 library."""

    #Coordinates of Image
    [image_left,image_top,image_right,image_bottom] = element.x0,element.y0,element.x1,element.y1
    #Cropping the image by using [left,bottom,right,top]

    pageObj.mediabox.lower_left = (image_left,image_bottom)
    pageObj.mediabox.upper_right = (image_right,image_top)

    #Saving the image PDF
    cropped_pdf_writter = PyPDF2.PdfWriter()
    cropped_pdf_writter.add_page(pageObj)

    with open('cropped_image.pdf','wb') as cropped_pdf_file:
        cropped_pdf_writter.write(cropped_pdf_file)


def convert_to_image(input_file):
    """Converts PDF file to Image"""
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_Image.png"
    image.save(output_file,"PNG")


def image_to_text(image_path):
    """Extract text from Image by pytesseract"""

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text



#Extracting Text From Tables
"""We can use Tabula but Disadvantges of Tabula is that 
1.when the library identifies the different 
rows of the table using the line-break special character \n in the table’s text.
So when text of column goes to other line it identifies it as row with NaN Columns

2.the extracted information is outputted in a Pandas DataFrame instead of a string. 
In most cases, this can be a desirable format but in the case of transformers that take into account text, 
these results need to be transformed before feeding into a model."""





def extract_tables(pdf_path, page_num, table_num):
    """Extracts tables from the PDF.
    
    Args:
        pdf_path (str): The path to the PDF file.
        page_num (int): The page number containing the table.
        table_num (int): The index of the table on the page.
    
    Returns:
        list: The extracted table as a list of lists.
    """
    pdf = pdfplumber.open(pdf_path)
    # Find the examined Page
    table_page = pdf.pages[page_num]
    # Extract the appropriate table
    tables = table_page.extract_tables()
    table = tables[table_num]
    return table

def table_converter(table):
    
    """1.We iterate in each nested list and clean its context from any unwanted line breaks coming from any wrapped text.
      2.We join each element of the row by separating them using the | symbol to create the structure of a table’s cell.
      3.Finally, we add a line break at the end to move to the next row."""

    table_string = ''

    for row_num,row in enumerate(table):
        processed_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]

        table_string += ('|' + '|'.join(processed_row) + '|' + '\n')

    table_string = table_string[:-1]  # Remove the last newline character

    return table_string
    

#Adding All the Functions Together
    

def final_extraction(pdf_path):
    text_per_page = {}
    with open(pdf_path,'rb') as pdf_file:
        read_pdf = PyPDF2.PdfReader(pdf_file)
    
        
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            pageObj = read_pdf.pages[pagenum]
            page_text,line_format,text_from_image,text_from_tables,page_content= [],[],[],[],[]
             
            table_num = 0
            first_element = True
            table_extraction_flag = False
            lower_side = 0
            upper_side = 0
            
            pdf = pdfplumber.open(pdf_path) #For Table Extraction
            page_tables = pdf.pages[pagenum]
            tables = page_tables.find_tables()
            
            # Find the elements in PDF Object for each page.
            page_elements = [(element.y1, element) for element in page._objs]
            page_elements.sort(key=lambda x: x[0], reverse=True)  
            """Sorting Acc to element.y1 as it ensure text is being shown as it is in PDF
            From Top to Bottom using y1 = top cordinate of element
            """
            for i, component in enumerate(page_elements):
                pos = component[0]  # Extracting Top Positions of Element
                element = component[1]
                
                if isinstance(element, LTTextContainer): #For Text in PDF
                    print("Found text container:", element)
                    (line_text, format_per_line) = text_extract(element)
                    page_text.append(line_text)
                    line_format.append(format_per_line)
                    

                elif isinstance(element, LTFigure):
                    print("Found figure:", element)
                    crop_image(element, pageObj)
                    convert_to_image('cropped_image.pdf')
                    image_text = image_to_text("PDF_Image.png")
                    text_from_image.append(image_text)
                    

                elif isinstance(element, LTRect): #For Tables
                    if first_element == True and (table_num+1)<=len(tables):
                        print(page.bbox[3])
                        lower_side = page.bbox[3] - tables[table_num].bbox[3]
                        upper_side = element.y1
                        table = extract_tables(pdf_path,pagenum,table_num)
                        table_string = table_converter(table)

                        text_from_tables.append(table_string)
                        

                        table_extraction_flag = True
                        first_element = False
                    # Check if we already extracted the tables from the page
                    if element.y0 >=lower_side and element.y1<=upper_side:
                        pass
                    elif not isinstance(page_elements[i+1][1],LTRect):
                        table_extraction_flag = False
                        first_element = True
                        table_num+=1

                    
            # Add the extracted data to the dictionary
            text_per_page[pagenum] = {
                "page_text": page_text,
                "text_from_image": text_from_image,
                "text_from_tables": text_from_tables,
                }
        
        return text_per_page

pdf_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\document-3a31866.pdf"
extracted_data = final_extraction(pdf_path)






















