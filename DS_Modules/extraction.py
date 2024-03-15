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

    line_text = element.get_text()  #Method of LTTEContrainer which extract words within the corpus box and store in a list
    
    line_formats = []

    for text_line in element:
        if isinstance(text_line,LTTextContainer):

            for char in text_line:
                if isinstance(char,LTChar):
                    line_formats.append(char.fontname)
                    line_formats.append(char.size)

    format_per_line = list(set(line_formats))
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
    cropped_pdf_writter = PyPDF2.PDFWriter()
    cropped_pdf_writter.add_page(pageObj)

    with open('cropped_image.pdf','wb') as cropped_pdf_file:
        cropped_pdf_writter.write(cropped_pdf_file)


def convert_to_image(input_file):
    """Converts PDF file to Image"""
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_Image.pdf"
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

def extract_tables(pdf_path,page_num,table_num):
    """1.Opens PDF from path navigates to the page_num 
    2.From the list of tables found on page by pdfplummber we select desired one
    3.We extract the content of the table and output it in a list of nested lists representing each row of the table.
    """

    pdf = pdfplumber.open(pdf_path)

    #Find the examined Page
    table_page = pdf.pages(page_num)

    #Extract the appropriate table
    table = table.extract_table()[table_num]

    return table


def table_converter(table):

    """1.We iterate in each nested list and clean its context from any unwanted line breaks coming from any wrapped text.
      2.We join each element of the row by separating them using the | symbol to create the structure of a table’s cell.
      3.Finally, we add a line break at the end to move to the next row."""
    table_string =''

    for row_num in range(len(table)):
        row = table[row_num]

        processed_row = [item.replace('\n',' ') if item not None and '\n' in item else 'None' if item is None for else item for item in row ]
        """For Example row = ["This is cell 1", "Cell 2\nwith a newline", None] then 
         processed_row = ["This is cell 1", "Cell 2 with a newline", "None"]"""
        
        table_string+=('|'+'|'.join(processed_row)+ '|'+'\n')
        table_string = table_string[:-1]
        return table_string
    

#Adding All the Functions Together
    
pdf_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\somatosensory.pdf"
pdfFileObj = open(pdf_path,'rb')
read_pdf = PyPDF2.PdfReader(pdfFileObj)

text_per_page = {}
pdf_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\somatosensory.pdf"
for pagenum,page in enumerate(extract_pages(pdf_path)):

    pageObj = read_pdf.pages[pagenum]
    page_text = []
    line_format = []
    text_from_image = []
    text_from_tables = []
    page_content = []

    table_num = 0
    first_element = True
    table_extraction = False

    pdf = pdfplumber.open(pdf_path)
    page_tables = pdf.pages[pagenum]
    tables = page_tables.find_tables()

    print(page_tables)




    """LTFigure which represents the area of the PDF that can present figures or 
images that have been embedded as another PDF document in the page.
LTTextContainer which represents a group of text lines in a rectangular area is 
then analysed further into a list of LTTextLine objects. Each one of them represents a list of 
LTChar objects, which store the single characters of text along with their metadata. (5)
LTRect represents a 2-dimensional rectangle that can be used to frame images, and 
figures or create tables in an LTPage object."""

    if isinstance(element,LTTextContainer):  #isinstance checks if elememt is LTTextContainer type
        #Function to extract the text from the text block


        #Function to extract the text format pass

    # if isinstance(element,LTFigure):

    #     #Function to convert PDFImage to PNG

    #     #Function to extract text from Images with OCR pass

    # if isinstance(element,LTRect):

    #     #Function to extract table pass

    #     #Function to convert Table Content to String





















