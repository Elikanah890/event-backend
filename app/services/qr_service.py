import qrcode
import os
import hashlib
from datetime import datetime
from app.core.config import QR_FOLDER_PATH, ensure_qr_folder_exists

ensure_qr_folder_exists()

def generate_invitation_qr(invitation_token: str) -> str:
    """
    Generate a QR code for the invitation token and save to disk.
    Returns the file path.
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(invitation_token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Use hash to avoid filename collisions
    qr_hash = hashlib.sha256(invitation_token.encode()).hexdigest()
    file_path = os.path.join(QR_FOLDER_PATH, f"{qr_hash}.png")
    img.save(file_path)
    return qr_hash, file_path
