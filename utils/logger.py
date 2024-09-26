import logging
import os

def setup_logging():
    """
    Sets up logging for the application. Logs are written to 'app.log' in the project root
    and also output to the console.
    """
    log_file = os.path.join(os.getcwd(), 'app.log')
    
    # Avoid duplicate handlers if setup_logging is called multiple times
    if not logging.getLogger().handlers:
        # Configure file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to the root logger
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(console_handler)
        logging.getLogger().setLevel(logging.INFO)


