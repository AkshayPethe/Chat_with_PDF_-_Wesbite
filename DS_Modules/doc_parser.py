import tabula
from unstructured.partition.pdf import partition_pdf

# def get_text_for_url(website_url):
#     try:
#         loader = WebBaseLoader(website_url)
#         documents = loader.load()
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error loading URL: {e}")
#         return None
    
#     return documents

# Assuming the file exists at the specified path
path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\ast_sci_data_tables_sample.pdf"
image_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\Images"




def extract_pdf_data(path, image_path):
    """Extracts text and tables from a PDF, saving images to a specified directory.

    Args:
        path (str): Path to the PDF file.
        image_path (str): Path to the directory for storing extracted images (optional).

    Returns:
        tuple: A tuple containing two lists:
            - text (list): A list of strings containing the extracted text elements.
            - tables (list): A list of dataframes extracted from the PDF tables using `tabula`.

    Raises:
        Exception: If an error occurs during PDF processing.
    """

    try:
     
        tables = tabula.read_pdf(
            path,
            multiple_tables=True,  
            lattice=True,     
            pandas_options={'dtype': str}, # Ensure string data type for tables
            pages = 'all'  
        )


        raw_pdf_elements = partition_pdf(
            filename=path,
            extract_images_in_pdf=bool(image_path), 
            image_output_dir_path=image_path,
            # Adjust chunking and combining options as needed
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000
        )

        text = []
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.CompositeElement" in str(type(element)):
                text.append(str(element))
            else:
                text = []

        return text, tables

    except Exception as e:
        print(f"Error occurred while extracting data from PDF: {e}")
        return [], []  # Return empty lists on error

if __name__ == "__main__":
    path =r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\ast_sci_data_tables_sample.pdf"  # Replace with the actual path to your PDF
    image_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\Images"  # Optional path for extracted images (if desired)

    text, tables = extract_pdf_data(path, image_path)

    # Process the extracted text and tables as needed
    print("Extracted Text:")
    for line in text:
        print(line)

    print("\nExtracted Tables:")
    for table in tables:
        print(table.to_string())



