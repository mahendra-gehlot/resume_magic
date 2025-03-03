import os

def save_tex(ai_gen_resume: str, location_to_save: str, file_name: str, remove_if_exists=False):
    """
    Save the generated LaTeX resume content to a .tex file.
    Optionally removes the file if it already exists.

    Args:
        ai_gen_resume (str): LaTeX formatted resume content.
        location_to_save (str): Path where the .tex file should be saved.
        remove_if_exists (bool): If True, removes the file at the location if it exists.
        
    Raises:
        Exception: If there's an error writing to or managing the file.
    """
    try:
        # Ensure the path ends with .tex
        if not location_to_save.endswith('.tex'):
            location_to_save += file_name
        
        # Remove the file if it exists and the flag is set
        if remove_if_exists and os.path.exists(location_to_save):
            try:
                os.remove(location_to_save)
                print(f"The existing file at '{location_to_save}' was removed.")
            except Exception as e:
                raise Exception(f"Error removing existing file: {e}")
        
        # Write the new LaTeX content to the file
        with open(location_to_save, 'w', encoding='utf-8') as f:
            f.write(ai_gen_resume)
        print(f"LaTeX file saved successfully at '{location_to_save}'.")
    
    except (IOError, OSError) as e:
        raise Exception(f"Error saving LaTeX file to {location_to_save}: {str(e)}")
