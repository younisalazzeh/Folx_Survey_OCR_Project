'use client';

import React from 'react';

interface ProcessingStatusProps {
  status: string;
  progress: number;
}

export default function ProcessingStatus({ status, progress }: ProcessingStatusProps) {
  // Convert status to user-friendly message
  const statusMessage = () => {
    switch (status) {
      case 'uploading':
        return 'Uploading image...';
      case 'processing':
        return 'Processing survey...';
      case 'completed':
        return 'Processing complete!';
      case 'error':
        return 'Error processing survey';
      default:
        return 'Waiting to start...';
    }
  };

  return (
    <div className="mt-4">
      <h3 className="text-lg font-medium mb-2">Processing Status</h3>
      <div className="bg-gray-100 rounded-full h-4 w-full">
        <div 
          className="bg-blue-500 h-4 rounded-full transition-all duration-300 ease-in-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="mt-2 text-sm text-gray-600">{statusMessage()}</p>
    </div>
  );
}
