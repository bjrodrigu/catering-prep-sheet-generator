from flask import *
import os

app = Flask(__name__) 

UPLOAD_FOLDER = '../user_receipts/' 
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
        return "Files Uploaded Successfully.!"
if __name__ == '__main__': 
    app.run(debug=True) 