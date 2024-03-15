import tabula
from unstructured.partition.pdf import partition_pdf

def extract_pdf_data(path):
    """Extracts text and tables from a PDF, saving images to a specified directory (optional).

    Args:
        path (str): Path to the PDF file.
        image_path (str): Path to the directory for storing extracted images (optional).

    Returns:
        list: A list containing the extracted elements from the PDF (potentially including text and table data).

    Raises:
        Exception: If an error occurs during PDF processing.
    """

    try:
        tables_tab = tabula.read_pdf(
            path,
            multiple_tables=True,
            lattice=True,
            pandas_options={'dtype': str},  # Ensure string data type for tables
            pages='all'
        )

        raw_pdf_elements = partition_pdf(
            filename=path,
            extract_images_in_pdf=True,
            # Adjust chunking and combining options as needed
            chunking_strategy="by_title",
            max_characters=2000,
            new_after_n_chars=1800,
            combine_text_under_n_chars=500
        )

        return tables_tab,raw_pdf_elements

    except Exception as e:
        print(f"Error occurred while extracting data from PDF: {e}")
        return [] 



def data_category(raw_pdf_elements):
    """Categorizes extracted PDF elements into tables and text.

    Args:
        raw_pdf_elements (list): List of elements extracted from the PDF using partition_pdf.

    Returns:
        list: A list containing two sub-lists:
            - texts (list): List of extracted text elements.
            - tables (list): List of extracted tables (converted to strings).
    """

    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            texts.append(str(element))
    data_category = [texts,tables]      

    return texts
"""Disadvantges of Tabula is that 1.when the library identifies the different 
rows of the table using the line-break special character \n in the table’s text.

2.the extracted information is outputted in a Pandas DataFrame instead of a string. 
In most cases, this can be a desirable format but in the case of transformers that take into account text, 
these results need to be transformed before feeding into a model."""

if __name__ == "__main__":
    path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\ast_sci_data_tables_sample.pdf"
    image_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\Images"

    tables,raw_pdf_elements = extract_pdf_data(path)
    print("a")

    # Unpack the returned list from data_category
    text = data_category(raw_pdf_elements)
    print("b")

    # Process the extracted text and tables as needed
    print("Extracted Text:")
    for line in text:
        print(line)

    print("\nExtracted Tables:")
    for table in tables:
        print(table.to_string())  # Assuming tables are DataFrames, use to_string
