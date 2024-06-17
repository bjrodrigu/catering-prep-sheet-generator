import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Header from './Header';

const App = () => {
  const [files, setFiles] = useState([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [visible, setVisible] = useState(false);

  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    console.log("Running handleSubmit")
    event.preventDefault();

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Files uploaded successfully:', response.data);
      setSuccessMessage('Files uploaded successfully!');
      setErrorMessage('');
      setVisible(false);
      console.log("Visible: ", visible)
      setTimeout(() => {
        setSuccessMessage('');
        setVisible(true);
      }, 3000);

    } catch (error) {
      console.error('Error uploading files:', error);
      setErrorMessage('Error uploading files. Please try again.');
      setSuccessMessage('');
      setTimeout(() => {
        setErrorMessage('');
      }, 3000); 
    }
  };

  function deleteFiles() {
    axios.post('/delete-files')
      .then(function (response) {
        console.log('Files deleted:', response.data.user_receipts, response.data.receipt_text_files);
      })
      .catch(function (error) {
        console.error('Error deleting files:', error.response.data.error);
      });
  }

  return (
    <div>
      <Header />
      <div className="file-upload-container">
        <form onSubmit={handleSubmit} className="file-upload-form">
          <input type="file" name="file" multiple onChange={handleFileChange} className="file-input" accept=".pdf,.jpg,.jpeg,.png" />
          <label htmlFor="file" className="file-label" style={{ fontSize: 'smaller', textAlign: 'center' }}>must be .pdf, .jpg, .jpeg, .png</label>
          <button type="submit" className="upload-button">Upload</button>
          {successMessage && <div className="success-message">{successMessage}</div>}
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          {visible && (
            <a href="/catering_execution_sheet.xlsx" download onClick={deleteFiles}>
              Download Excel Sheet
            </a>
          )}
          <label htmlFor="file" className="file-label" style={{ fontSize: 'smaller', textAlign: 'center' }}>Make sure to upload all receipts prior to downloading file</label>
        </form>
      </div>
    </div>
  );
};

export default App;
