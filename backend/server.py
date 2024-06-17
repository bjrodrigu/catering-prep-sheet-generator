from flask import *
import os
import subprocess


app = Flask(__name__) 

UPLOAD_FOLDER = 'user_receipts/' 
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
  
@app.route('/') 
def main(): 
    return render_template("index.html") 
  
@app.route('/upload', methods=['POST']) 
def upload(): 
    if request.method == 'POST': 
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
        # Iterate for each file in the files List, and Save them 
        for file in files: 
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

        result = subprocess.run(['python', 'Spreadsheetmaker.py'], capture_output=True, text=True)

        return f"Process completed. \nScript Output: \n{result.stdout}\nScript Errors: \n{result.stderr}"
    
@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        # List files in the directory
        list_files_process_1 = subprocess.run(['ls', 'user_receipts/'], capture_output=True, text=True)
        list_files_process_2 = subprocess.run(['ls', 'receipt_text_files/'], capture_output=True, text=True)
        
        # Perform deletion
        subprocess.run('rm user_receipts/*', shell=True)
        subprocess.run('rm receipt_text_files/*', shell=True)
        subprocess.run('rm ../frontend/public/catering_execution_sheet.xlsx', shell=True)

        return jsonify({'user_receipts': list_files_process_1.stdout, 'receipt_text_files': list_files_process_2.stdout})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__': 
    app.run(debug=True) 