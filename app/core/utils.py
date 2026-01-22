import os
from app.core.config import QR_FOLDER_PATH

def ensure_qr_folder_exists():
    if not os.path.exists(QR_FOLDER_PATH):
        os.makedirs(QR_FOLDER_PATH, exist_ok=True)
