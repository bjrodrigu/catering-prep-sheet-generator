import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Header from './Header';

const App = () => {
  const [files, setFiles] = useState([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
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
      setTimeout(() => {
        setSuccessMessage('');
      }, 5000); // Clear the message after 5 seconds
    } catch (error) {
      console.error('Error uploading files:', error);
      setErrorMessage('Error uploading files. Please try again.');
      setSuccessMessage('');
      setTimeout(() => {
        setErrorMessage('');
      }, 5000); // Clear the message after 5 seconds
    }
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
        </form>
      </div>
    </div>
  );
};

export default App;
