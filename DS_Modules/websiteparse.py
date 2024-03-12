import os

from unstructured.partition.pdf import partition_pdf


# Assuming the file exists at the specified path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser #Takes Ouptput from model and convert it into string

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def table_summarize(tables):
    prompt_text = """You are an assistant tasked with summarizing tables. \
                    Give a concise summary of the table.Also Summarize each datapoint in a table. Table chunk: {element} """

    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

    return table_summaries




image_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\Images"
path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\ast_sci_data_tables_sample.pdf"
raw_pdf_elements = partition_pdf(
    filename=path,
    extract_images_in_pdf=True,
    image_output_dir_path=image_path,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=2000,

)


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

    return [texts, tables]
texts,tables = data_category(raw_pdf_elements)
print(texts)

table_summarize = table_summarize(tables)

print("*"*50)
print(table_summarize)
print("*"*50)
print(tables)
print("*"*50)
print(texts)