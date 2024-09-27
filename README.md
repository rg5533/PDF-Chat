 # 📄💬 Chat with PDF

Welcome to **Chat with PDF**! This application allows you to upload PDF documents and interact with their content using a chat interface powered by OpenAI and ChromaDB. Whether you're a data scientist, researcher, or anyone who works with PDFs, this tool can help you extract information and get answers to your questions seamlessly.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **PDF Upload:** Easily upload PDF files through a user-friendly interface.
- **Text Extraction:** Extracts text from PDFs using PyMuPDF.
- **Text Chunking:** Splits extracted text into manageable chunks for efficient processing.
- **Knowledge Base:** Stores and organizes extracted text using ChromaDB.
- **Interactive Chat:** Ask questions about your PDFs and receive intelligent responses powered by OpenAI.
- **Logging:** Comprehensive logging for monitoring and debugging.

## Demo

![Chat with PDF Demo](demo.gif)

*Screenshot of the application in action.*

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

bash
git clone https://github.com/yourusername/chat-with-pdf.git
cd chat-with-pdf

### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate


### 3. Activate the Virtual Environment

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies

bash
pip install -r requirements.txt



### 5. Set Up Environment Variables

Create a `.env` file in the root directory and add the following variables:

env
OPENAI_API_KEY=your_openai_api_key
CHROMADB_API_KEY=your_chromadb_api_key


*Replace `your_openai_api_key` and `your_chromadb_api_key` with your actual API keys.*

## Usage

Run the application using Streamlit:

bash
streamlit run app.py


Once the app is running:

1. **Upload PDF:** Navigate to the sidebar and upload your PDF file.
2. **Ask Questions:** Use the chat interface to ask questions about your PDF's content.
3. **Receive Answers:** Get intelligent responses based on the information extracted from your PDF.

## Project Structure

Here's a brief overview of the project's structure:


chat-with-pdf/
├── app.py
├── utils/
│ ├── pdf_processor.py
│ ├── vector_store.py
│ ├── openai_connector.py
│ └── logger.py
├── requirements.txt
├── .gitignore
├── README.md
└── paths_to_remove.txt


- **app.py:** Main application file that sets up the Streamlit interface and handles user interactions.
- **utils/pdf_processor.py:** Module for extracting text from PDF files.
- **utils/vector_store.py:** Handles interactions with ChromaDB for storing and querying text chunks.
- **utils/openai_connector.py:** Connects to OpenAI's API to generate responses based on user queries.
- **utils/logger.py:** Configures logging for the application.
- **.gitignore:** Specifies files and directories to be ignored by Git.
- **paths_to_remove.txt:** List of paths to be removed from version control.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository:** Click the fork button at the top right of this page.
2. **Create a Branch:** `git checkout -b feature/YourFeature`
3. **Commit Your Changes:** `git commit -m "Add some feature"`
4. **Push to the Branch:** `git push origin feature/YourFeature`
5. **Open a Pull Request:** Describe your changes and submit.

Please ensure your code follows the project's coding standards and includes appropriate comments.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact
Rohit Gupta
Email: rohitgupta5533@gmail.com
GitHub: rg5533

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the intuitive web framework.
- [OpenAI](https://openai.com/) for the powerful language models.
- [ChromaDB](https://www.chromadb.com/) for the efficient vector database.
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) for PDF text extraction.

---

Developed with ❤️ using Streamlit, OpenAI, and ChromaDB.


