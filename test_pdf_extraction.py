# test_pdf_extraction.py

import os
from utils.pdf_processor import extract_text_from_pdf
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_extraction(pdf_filename):
    """
    Tests the PDF text extraction process.
    
    :param pdf_filename: Name of the PDF file in the root directory.
    """
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file '{pdf_filename}' does not exist in the root directory.")
        return
    
    text = extract_text_from_pdf(pdf_path)
    if text:
        # Optionally, save the extracted text to a file for manual inspection
        extracted_text_path = os.path.join(os.getcwd(), "extracted_text.txt")
        with open(extracted_text_path, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Extracted text saved to {extracted_text_path}.")
    else:
        logger.warning("No text extracted from the PDF.")

if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the actual PDF filename
    test_extraction(r'C:\Users\rohit\VSCode\ChatWithPdf\Data Scientist - LSP.pdf')
