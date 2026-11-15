import glob
import os
import subprocess
import sys

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'user_receipts')
TEXT_FOLDER = os.path.join(BASE_DIR, 'receipt_text_files')
OUTPUT_SHEET = os.path.join(BASE_DIR, '..', 'frontend', 'public', 'catering_execution_sheet.xlsx')
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("file")
    saved = 0
    for file in files:
        # secure_filename strips path components so uploads can't escape UPLOAD_FOLDER
        filename = secure_filename(file.filename or '')
        if not filename or os.path.splitext(filename)[1].lower() not in ALLOWED_EXTENSIONS:
            continue
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        saved += 1

    if saved == 0:
        return jsonify({'error': 'No PDF or image files were uploaded.'}), 400

    result = subprocess.run(
        [sys.executable, 'SpreadsheetMaker.py'],
        capture_output=True, text=True, cwd=BASE_DIR,
    )
    return f"Process completed. \nScript Output: \n{result.stdout}\nScript Errors: \n{result.stderr}"


@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        removed = {}
        for name, folder in (('user_receipts', UPLOAD_FOLDER), ('receipt_text_files', TEXT_FOLDER)):
            paths = sorted(glob.glob(os.path.join(folder, '*')))
            for path in paths:
                if os.path.isfile(path):
                    os.remove(path)
            removed[name] = '\n'.join(os.path.basename(p) for p in paths)

        if os.path.isfile(OUTPUT_SHEET):
            os.remove(OUTPUT_SHEET)

        return jsonify(removed)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # 5000 matches the "proxy" in frontend/package.json; hosts like Railway set PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
