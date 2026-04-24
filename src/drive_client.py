import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GoogleDriveClient:
    def __init__(self, service_account_file: str, root_folder_name: str):
        if not os.path.exists(service_account_file):
            raise FileNotFoundError("Service account JSON nem található")

        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        self.service = build("drive", "v3", credentials=self.credentials)
        self.root_folder_name = root_folder_name

    def _get_or_create_folder(self, name, parent_id=None):
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])

        if files:
            return files[0]["id"]

        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")

    def upload_json(self, filepath: str) -> str:
        root_id = self._get_or_create_folder(self.root_folder_name)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        subfolder_id = self._get_or_create_folder(timestamp, root_id)

        file_metadata = {
            "name": os.path.basename(filepath),
            "parents": [subfolder_id],
        }

        media = MediaFileUpload(filepath, mimetype="application/json")
        file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        return file.get("id")
