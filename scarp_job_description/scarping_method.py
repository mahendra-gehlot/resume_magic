import os

def get_job_text(file_path):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be accessed due to insufficient permissions.
        Exception: For any other issues that occur while reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at '{file_path}' was not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied to read the file at '{file_path}'.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")


