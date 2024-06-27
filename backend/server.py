from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

UPLOAD_FOLDER = 'user_receipts/'
OUTPUT_FOLDER = 'frontend/build'
EXCEL_FILENAME = 'catering_execution_sheet.xlsx'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Serve React App
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve Static Files (React)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the list of files from the webpage
        files = request.files.getlist("file")
        # Iterate for each file in the files list, and save them
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

        # Run the external script
        result = subprocess.run(['python', 'backend/Spreadsheetmaker.py'], capture_output=True, text=True)

        # Check if the Excel file exists
        excel_file_path = os.path.join(OUTPUT_FOLDER, EXCEL_FILENAME)
        if os.path.exists(excel_file_path):
            return jsonify({
                "message": "Process completed.",
                "output_file": EXCEL_FILENAME,
                "script_output": result.stdout,
                "script_errors": result.stderr
            })
        else:
            return jsonify({
                "message": "Process completed but file not found.",
                "script_output": result.stdout,
                "script_errors": result.stderr
            }), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        # List files in the directories
        list_files_process_1 = subprocess.run(['ls', UPLOAD_FOLDER], capture_output=True, text=True)
        list_files_process_2 = subprocess.run(['ls', 'receipt_text_files/'], capture_output=True, text=True)
        
        # Perform deletion
        subprocess.run(['rm', '-f', os.path.join(UPLOAD_FOLDER, '*')], shell=True)
        subprocess.run(['rm', '-f', 'receipt_text_files/*'], shell=True)
        subprocess.run(['rm', '-f', os.path.join(OUTPUT_FOLDER, EXCEL_FILENAME)], shell=True)

        return jsonify({'user_receipts': list_files_process_1.stdout, 'receipt_text_files': list_files_process_2.stdout})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5956)))
