import React, { useState } from 'react';
import axios from 'axios';

function ImageUploader() {
  const [image, setImage] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [textQuery, setTextQuery] = useState('');

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setImage(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleQuery = () => {
    const formData = new FormData();
    formData.append('text', textQuery);

    // Send the image to the endpoint
    axios
      .post('http://localhost:8000/api_gateway/query', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(response => {
        console.log('Text sent successfully:', response.data);
      })
      .catch(error => {
        console.error('Error sending text:', error);
      });
    
    setTextQuery('');
  };

  const handleSentImage = () => {
    // Convert the data URL to Blob
    const dataURLtoBlob = (dataURL) => {
      const arr = dataURL.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    };

    // Convert the data URL to Blob
    const blob = dataURLtoBlob(image);

    // Create a FormData object to send the image, name, and description as multipart/form-data
    const formData = new FormData();
    formData.append('file', blob, 'image.jpg');
    formData.append('name', name);
    formData.append('description', description);

    // Send the image to the endpoint
    axios
      .post('http://localhost:8000/api_gateway/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
        console.log('Image saved successfully:', response.data);
      })
      .catch((error) => {
        console.error('Error saving image:', error);
      });
    setImage('');
    setDescription('');
    setName('');
  };
  return (
    <div>
      <h1>Image Uploader</h1>
      <input type="file" onChange={handleImageUpload} />
      <input
        type="text"
        placeholder="Image Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <textarea
        placeholder="Image Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      ></textarea>
      <textarea
        placeholder="Text Query"
        value={textQuery}
        onChange={(e) => setTextQuery(e.target.value)}
      ></textarea>
      {image && <img src={image} alt="Uploaded" />}
      {image && <button onClick={handleSentImage}>Save Image</button>}
      {textQuery && <button onClick={handleQuery}>Send Query</button>}
    </div>
  );
}

export default ImageUploader;