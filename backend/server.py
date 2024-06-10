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

        result = subprocess.run(['python', 'backend/Spreadsheetmaker.py'], capture_output=True, text=True)

        return f"Process completed. \nScript Output: \n{result.stdout}\nScript Errors: \n{result.stderr}"

if __name__ == '__main__': 
    app.run(debug=True) 