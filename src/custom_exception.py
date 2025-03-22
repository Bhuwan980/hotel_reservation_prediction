import sys
import traceback

class CustomException(Exception):
    """
    Custom Exception that captures and displays detailed traceback information.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)
        
    @staticmethod
    def get_detailed_error_message(self, error_message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        tb_info = traceback.extract_tb(exc_tb)
        if tb_info:
            file_name, line_number, func_name, _ = tb_info[-1]  # Last call in the traceback
            detailed_message = (
                f"Error: {error_message} | "
                f"File: {file_name} | "
                f"Line: {line_number} | "
                f"Function: {func_name}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            return detailed_message
        else:
            return f"Error: {error_message}"

    def __str__(self):
        return self.error_message