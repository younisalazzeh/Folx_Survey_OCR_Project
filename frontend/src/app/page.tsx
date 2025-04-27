'use client';

import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Survey OCR System</h1>
        <p className="text-xl mb-8">
          Upload survey images, extract data, and visualize results
        </p>
        
        <div className="flex justify-center gap-4">
          <Link 
            href="/upload"
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition-colors"
          >
            Upload Survey
          </Link>
          <Link 
            href="/dashboard"
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-lg transition-colors"
          >
            View Dashboard
          </Link>
        </div>
      </div>
      
      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">OCR Processing</h2>
          <p>Upload survey images and extract data using advanced OCR technology</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Data Visualization</h2>
          <p>View interactive charts and graphs of your survey results</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2">Export & Share</h2>
          <p>Export results in various formats or share with team members</p>
        </div>
      </div>
    </div>
  );
}
