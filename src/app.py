from flask import Flask, jsonify
from flask_cors import CORS
import json, os
from datetime import datetime
from config import settings
from garmin_client import GarminExtractorClient
from drive_client import GoogleDriveClient

app = Flask(__name__)
CORS(app)

@app.route('/')
def health():
    return jsonify({"status":"running"})

@app.route('/test-garmin')
def test_garmin():
    try:
        client = GarminExtractorClient(settings.garmin_email, settings.garmin_password)
        client.login()
        return jsonify({"status":"OK"})
    except Exception as e:
        return jsonify({"status":"ERROR","message":str(e)})

@app.route('/test-drive')
def test_drive():
    try:
        GoogleDriveClient(settings.google_service_account_file, settings.drive_root_folder_name)
        return jsonify({"status":"OK"})
    except Exception as e:
        return jsonify({"status":"ERROR","message":str(e)})

@app.route('/run')
def run():
    try:
        client = GarminExtractorClient(settings.garmin_email, settings.garmin_password)
        data = client.collect_last_days(settings.days_back)

        os.makedirs(settings.output_dir, exist_ok=True)
        filename = f"garmin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(settings.output_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        drive = GoogleDriveClient(settings.google_service_account_file, settings.drive_root_folder_name)
        file_id = drive.upload_json(filepath)

        return jsonify({"status":"OK","file":filename,"drive_id":file_id})

    except Exception as e:
        return jsonify({"status":"ERROR","message":str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
