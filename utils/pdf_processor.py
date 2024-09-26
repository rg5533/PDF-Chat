from utils.logger import setup_logging

# Initialize logging
setup_logging()
import fitz  # PyMuPDF
import logging

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string, or None if extraction fails.
    """
    try:
        logging.info(f"Extracting text from: {pdf_path}")
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text += page_text
            else:
                logging.warning(f"No text found on page {page_num + 1} of {pdf_path}.")
        doc.close()
        if not text.strip():
            logging.error(f"Extracted text is empty for {pdf_path}.")
            return None
        logging.info(f"Successfully extracted text from {pdf_path}. Length: {len(text)} characters.")
        return text
    except Exception as e:
        logging.error(f"An error occurred while extracting text from PDF: {e}")
        return None

