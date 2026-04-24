import os
import base64
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def ensure_service_account_file(path: str) -> str:
    raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    raw_b64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_B64", "")

    if raw_json and not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(raw_json)

    if raw_b64 and not os.path.exists(path):
        decoded = base64.b64decode(raw_b64).decode("utf-8")
        with open(path, "w", encoding="utf-8") as f:
            f.write(decoded)

    return path


@dataclass
class Settings:
    garmin_email: str = os.getenv("GARMIN_EMAIL", "")
    garmin_password: str = os.getenv("GARMIN_PASSWORD", "")
    google_service_account_file: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    drive_root_folder_name: str = os.getenv("DRIVE_ROOT_FOLDER_NAME", "Garmin Daily Data")
    days_back: int = int(os.getenv("DAYS_BACK", "30"))
    output_dir: str = os.getenv("OUTPUT_DIR", "output")
    api_key: str = os.getenv("API_KEY", "")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    def prepare(self):
        self.google_service_account_file = ensure_service_account_file(self.google_service_account_file)
        return self


settings = Settings().prepare()
