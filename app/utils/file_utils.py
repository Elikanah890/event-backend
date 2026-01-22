import os

def ensure_folder_exists(folder_path: str):
    """
    Ensure the folder exists; create if not.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
