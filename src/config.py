import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    garmin_email: str = os.getenv("GARMIN_EMAIL", "")
    garmin_password: str = os.getenv("GARMIN_PASSWORD", "")
    google_service_account_file: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    drive_root_folder_name: str = os.getenv("DRIVE_ROOT_FOLDER_NAME", "Garmin Daily Data")
    days_back: int = int(os.getenv("DAYS_BACK", "30"))
    output_dir: str = os.getenv("OUTPUT_DIR", "output")

settings = Settings()
