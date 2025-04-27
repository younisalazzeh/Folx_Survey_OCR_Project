'use client';

import React from 'react';

interface ImagePreviewProps {
  imageUrl: string | null;
}

export default function ImagePreview({ imageUrl }: ImagePreviewProps) {
  if (!imageUrl) return null;
  
  return (
    <div className="mt-4">
      <h3 className="text-lg font-medium mb-2">Image Preview</h3>
      <div className="border rounded-lg overflow-hidden">
        <img 
          src={imageUrl} 
          alt="Survey preview" 
          className="max-w-full h-auto"
        />
      </div>
    </div>
  );
}
