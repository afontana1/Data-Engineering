import React, { useState } from 'react';
import axios from 'axios';

const VideoUploader = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('video', file);

    const response = await axios.post('/upload', formData);

    if (response.status === 200) {
      console.log('Video uploaded successfully!');
    } else {
      console.log('Error uploading video.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleFileChange} />
      <button type="submit">Upload Video</button>
    </form>
  );
};

export default VideoUploader;