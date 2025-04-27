'use client';

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface ImageUploaderProps {
  onUpload: (file: File, preview: string) => Promise<void>;
}

export default function ImageUploader({ onUpload }: ImageUploaderProps) {
  const [isUploading, setIsUploading] = useState(false);
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    setIsUploading(true);
    try {
      // Preview logic
      const file = acceptedFiles[0];
      const preview = URL.createObjectURL(file);
      
      // Call the onUpload callback with the file and preview
      await onUpload(file, preview);
    } catch (error) {
      console.error('Upload error:', error);
      // Handle error state
    } finally {
      setIsUploading(false);
    }
  }, [onUpload]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.tiff']
    },
    maxFiles: 1
  });
  
  return (
    <div className="w-full">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
      >
        <input {...getInputProps()} />
        {isUploading ? (
          <p>Uploading...</p>
        ) : isDragActive ? (
          <p>Drop the survey image here...</p>
        ) : (
          <div>
            <p>Drag and drop a survey image, or click to select</p>
            <p className="text-sm text-gray-500 mt-2">Supported formats: JPEG, PNG, TIFF</p>
          </div>
        )}
      </div>
    </div>
  );
}
