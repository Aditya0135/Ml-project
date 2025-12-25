import sys  # Import system-specific parameters and functions
from src.logger import logging
logger= logging.getLogger(__name__)

# Function to format detailed error messages
def error_message_detail(error, error_detail: sys):
    # Get the most recent exception info as a tuple (type, value, traceback)
    _, _, exc_tb = error_detail.exc_info()
    
    # Extract the file name where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Create a formatted error message with file, line number, and original error
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    
    return error_message  # Return the formatted error message


# Custom exception class to include detailed error information
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # Call the parent Exception class constructor with the raw error message
        super().__init__(error_message)
        
        # Store the formatted detailed error message in the object
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    # Override string representation so printing the exception shows the detailed message
    def __str__(self):
        return self.error_message
    
if __name__ =="__main__":
    try:
        1/0
    except Exception as e:
        logging.info("Division by zero")
        raise CustomException(e,sys) # whole error in e take error from sys
        

