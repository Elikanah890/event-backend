from dotenv import load_dotenv
import os

# Load .env file automatically
load_dotenv()

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://eventapp:StrongPassword123!@localhost:3306/event_management"
)

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-this")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))  # 24 hours default

# QR settings
QR_FOLDER_PATH = os.getenv("QR_FOLDER_PATH", "app/static/qr_codes")  # folder to store QR images

def ensure_qr_folder_exists():
    """
    Ensure the QR code folder exists in the project.
    Creates it if it doesn't exist.
    """
    if not os.path.exists(QR_FOLDER_PATH):
        os.makedirs(QR_FOLDER_PATH)
