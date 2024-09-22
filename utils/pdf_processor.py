import PyPDF2

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"Extracting text from: {pdf_path}")  # Debugging line

    """
    Extracts text from a PDF file.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a single string.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
    except PyPDF2.errors.PdfReadError as e:
        print(f"PDF read error: {e}")
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
    return text

