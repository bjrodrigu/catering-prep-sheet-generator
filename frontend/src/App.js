import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Header from './Header';

const App = () => {
  const [files, setFiles] = useState([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [visible, setVisible] = useState(false);
  const [downloadLink, setDownloadLink] = useState('');

  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    console.log("Running handleSubmit");
    event.preventDefault();

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log("Backend URL:", process.env.REACT_APP_BACKEND_URL);
      console.log('Response Data:', response.data);
      
      if (response.data.output_file) {
        setDownloadLink(`${process.env.REACT_APP_BACKEND_URL}/download/${response.data.output_file}`);
        setSuccessMessage('Files uploaded successfully!');
        setErrorMessage('');
        setVisible(true);
      } else {
        setErrorMessage('File not generated.');
        setSuccessMessage('');
        setVisible(false);
      }
    } catch (error) {
      console.error('Error uploading files:', error);
      setErrorMessage('Error uploading files. Please try again.');
      setSuccessMessage('');
      setVisible(false);
    }
  };

  const deleteFiles = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/delete-files`)
      .then(response => {
        console.log('Files deleted:', response.data.user_receipts, response.data.receipt_text_files);
      })
      .catch(error => {
        console.error('Error deleting files:', error.response.data.error);
      });
  };

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
            <a href={downloadLink} download onClick={deleteFiles}>
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
