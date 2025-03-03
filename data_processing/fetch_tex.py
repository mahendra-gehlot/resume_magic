
import os

def read_latex_file(file_path = './data/current_resume.tex'):
    """
    Reads a LaTeX file and returns its content as a formatted string.

    Args:
        file_path (str): The path to the LaTeX file.

    Returns:
        str: The formatted content of the LaTeX file.
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # Return the formatted string
        return content.strip()
    except FileNotFoundError:
        return f"Error: The file at '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"