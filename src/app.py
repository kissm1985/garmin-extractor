from flask import Flask, request, jsonify, render_template_string
import json, os
from datetime import datetime
from config import settings
from garmin_client import GarminExtractorClient
from drive_client import GoogleDriveClient

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Garmin Extractor</title>
<style>
body{font-family:Arial;padding:20px;background:#f4f6f8}
.card{background:white;padding:20px;border-radius:10px;margin-bottom:10px}
button{padding:10px 15px;background:#2563eb;color:white;border:none;border-radius:6px;cursor:pointer}
</style>
</head>
<body>
<h1>Garmin Extractor UI</h1>

<div class='card'>
<h3>1. Garmin Login teszt</h3>
<button onclick="testGarmin()">Teszt</button>
<p id='garmin'></p>
</div>

<div class='card'>
<h3>2. Google Drive kapcsolat</h3>
<button onclick="testDrive()">Teszt</button>
<p id='drive'></p>
</div>

<div class='card'>
<h3>3. Adat letöltés + feltöltés</h3>
<button onclick="runExtract()">Futtatás</button>
<p id='result'></p>
</div>

<script>
async function testGarmin(){
 const r = await fetch('/test-garmin');
 const j = await r.json();
 document.getElementById('garmin').innerText = JSON.stringify(j);
}
async function testDrive(){
 const r = await fetch('/test-drive');
 const j = await r.json();
 document.getElementById('drive').innerText = JSON.stringify(j);
}
async function runExtract(){
 const r = await fetch('/run');
 const j = await r.json();
 document.getElementById('result').innerText = JSON.stringify(j);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

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
    app.run(debug=True)
