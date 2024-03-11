import os
import io
import uuid
import base64
from base64 import b64decode
import numpy as np
import time
from PIL import Image
from unstructured.partition.pdf import partition_pdf

# Assuming the file exists at the specified path
path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\IF10244.pdf"
image_path = r"C:\Users\asus\OneDrive\Desktop\GenAI\AdvancedRag\Images"
poppler_path = r"C:\Program Files\poppler-24.02.0\Library\bin"
file_name = "plant-design-final.pdf"
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