from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)  # Enable CORS if needed

UPLOAD_FOLDER = 'user_receipts/'
OUTPUT_FILE_PATH = '../frontend/public/catering_execution_sheet.xlsx'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Serve React App
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve Static Files (React)
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the list of files from the webpage
        files = request.files.getlist("file")
        # Iterate for each file in the files list, and save them
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

        # Run the external script
        result = subprocess.run(['python', 'backend/Spreadsheetmaker.py'], capture_output=True, text=True)
        
        return jsonify({
            "message": "Process completed.",
            "script_output": result.stdout,
            "script_errors": result.stderr
        })
    
    except Exception as e:
        logging.error(f"Error during upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        # List files in the directories
        list_files_process_1 = subprocess.run(['ls', UPLOAD_FOLDER], capture_output=True, text=True)
        list_files_process_2 = subprocess.run(['ls', 'receipt_text_files/'], capture_output=True, text=True)

        
        # Perform deletion
        subprocess.run(['rm', '-f', os.path.join(UPLOAD_FOLDER, '*')], check=True)
        subprocess.run(['rm', '-f', 'receipt_text_files/*'], shell=True)
        subprocess.run(['rm', '-f', OUTPUT_FILE_PATH], check=True)
        
        return jsonify({
            'user_receipts': list_files_process_1.stdout,
            'receipt_text_files': list_files_process_2.stdout
        })
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error during deletion: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f"General error during deletion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
