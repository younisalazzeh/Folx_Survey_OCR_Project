# Step-by-Step Implementation Guide for Survey OCR Project

This guide provides detailed instructions for implementing the Survey OCR project from start to finish. The project is a web application that allows users to upload images of surveys with filled dots/bubbles, processes them using OCR and computer vision, and generates visualizations of the results.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Frontend Implementation](#2-frontend-implementation)
3. [Backend Implementation](#3-backend-implementation)
4. [OCR and Image Processing](#4-ocr-and-image-processing)
5. [Data Analysis and Visualization](#5-data-analysis-and-visualization)
6. [Integration and Testing](#6-integration-and-testing)
7. [Deployment](#7-deployment)

## 1. Project Setup

### 1.1 Environment Setup

#### 1.1.1 Create Project Directory Structure
```bash
mkdir -p survey-ocr-project/{frontend,backend}
cd survey-ocr-project
```

#### 1.1.2 Set Up Version Control
```bash
git init
echo "node_modules/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "uploads/" >> .gitignore
echo "processed/" >> .gitignore
git add .gitignore
git commit -m "Initial commit: Add .gitignore"
```

### 1.2 Frontend Project Initialization

#### 1.2.1 Create Next.js Project
```bash
cd frontend
npx create-next-app@latest .
```
When prompted, select the following options:
- Use TypeScript: No
- Use ESLint: Yes
- Use Tailwind CSS: Yes
- Use `src/` directory: Yes
- Use App Router: Yes
- Customize default import alias: No

#### 1.2.2 Install Additional Dependencies
```bash
npm install axios react-dropzone recharts
```

### 1.3 Backend Project Initialization

#### 1.3.1 Create Python Virtual Environment
```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 1.3.2 Install Backend Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic python-multipart opencv-python pytesseract easyocr numpy pandas scikit-learn scipy pillow
```

#### 1.3.3 Create Requirements File
```bash
pip freeze > requirements.txt
```

#### 1.3.4 Create Basic Project Structure
```bash
mkdir -p app/{api/routes,core,db/models,schemas,services/{ocr,analysis,rpa},utils}
touch app/__init__.py app/main.py app/config.py
touch app/api/__init__.py app/api/routes/__init__.py
touch app/core/__init__.py app/core/config.py
touch app/db/__init__.py app/db/session.py app/db/base.py
touch app/db/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/services/ocr/__init__.py
touch app/services/analysis/__init__.py
touch app/services/rpa/__init__.py
touch app/utils/__init__.py
```

## 2. Frontend Implementation

### 2.1 Project Structure Setup

#### 2.1.1 Create Component Directories
```bash
cd ../frontend
mkdir -p src/components/{common,upload,visualization,dashboard}
mkdir -p src/hooks
mkdir -p src/lib
mkdir -p src/context
```

#### 2.1.2 Create Basic Pages
Create the following files:

**src/app/page.js**
```jsx
import Link from 'next/link';

export default function Home() {
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
```

**src/app/layout.js**
```jsx
import './globals.css';

export const metadata = {
  title: 'Survey OCR System',
  description: 'Process survey images using OCR and visualize results',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav className="bg-blue-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <a href="/" className="text-xl font-bold">Survey OCR</a>
            <div className="space-x-4">
              <a href="/upload" className="hover:underline">Upload</a>
              <a href="/dashboard" className="hover:underline">Dashboard</a>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}
```

**src/app/upload/page.js**
```jsx
'use client';

export default function UploadPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Upload Survey Image</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <p>Upload component will be implemented here</p>
      </div>
    </div>
  );
}
```

**src/app/dashboard/page.js**
```jsx
'use client';

export default function DashboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Survey Results Dashboard</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <p>Dashboard components will be implemented here</p>
      </div>
    </div>
  );
}
```

### 2.2 Implement Common Components

#### 2.2.1 Create Button Component
**src/components/common/Button.jsx**
```jsx
export default function Button({ 
  children, 
  onClick, 
  type = 'button', 
  variant = 'primary', 
  className = '' 
}) {
  const baseClasses = 'px-4 py-2 rounded-lg transition-colors';
  
  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-600 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    danger: 'bg-red-500 hover:bg-red-600 text-white',
  };
  
  return (
    <button
      type={type}
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
```

#### 2.2.2 Create Card Component
**src/components/common/Card.jsx**
```jsx
export default function Card({ children, title, className = '' }) {
  return (
    <div className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`}>
      {title && (
        <div className="border-b px-6 py-3">
          <h3 className="text-lg font-medium">{title}</h3>
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
```

### 2.3 Implement Upload Components

#### 2.3.1 Create API Client
**src/lib/api.js**
```jsx
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getProcessingStatus = async (surveyId) => {
  const response = await apiClient.get(`/status/${surveyId}`);
  return response.data;
};

export const getSurveyResults = async (surveyId) => {
  const response = await apiClient.get(`/results/${surveyId}`);
  return response.data;
};

export default apiClient;
```

#### 2.3.2 Create Image Uploader Component
**src/components/upload/ImageUploader.jsx**
```jsx
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

export default function ImageUploader({ onUpload }) {
  const [isUploading, setIsUploading] = useState(false);
  
  const onDrop = useCallback(async (acceptedFiles) => {
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
      'image/*': ['.jpeg', '.jpg', '.png', '.tiff', '.pdf']
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
            <p className="text-sm text-gray-500 mt-2">Supported formats: JPEG, PNG, TIFF, PDF</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

#### 2.3.3 Create Image Preview Component
**src/components/upload/ImagePreview.jsx**
```jsx
export default function ImagePreview({ imageUrl }) {
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
```

#### 2.3.4 Create Processing Status Component
**src/components/upload/ProcessingStatus.jsx**
```jsx
export default function ProcessingStatus({ status, progress }) {
  return (
    <div className="mt-4">
      <h3 className="text-lg font-medium mb-2">Processing Status</h3>
      <div className="bg-gray-100 rounded-full h-4 w-full">
        <div 
          className="bg-blue-500 h-4 rounded-full transition-all duration-300 ease-in-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="mt-2 text-sm text-gray-600">{status}</p>
    </div>
  );
}
```

#### 2.3.5 Create Custom Hook for Image Processing
**src/hooks/useImageProcessing.js**
```jsx
import { useState } from 'react';
import { uploadImage, getProcessingStatus } from '../lib/api';

export function useImageProcessing() {
  const [status, setStatus] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  const processImage = async (file) => {
    setStatus('uploading');
    setProgress(10);
    setError(null);
    
    try {
      // Upload the image
      setStatus('uploading');
      const uploadResponse = await uploadImage(file);
      
      const { id } = uploadResponse;
      
      // Poll for processing status
      setStatus('processing');
      let processingComplete = false;
      
      while (!processingComplete) {
        const statusResponse = await getProcessingStatus(id);
        const { status: processingStatus, progress: processingProgress } = statusResponse;
        
        setProgress(50 + (processingProgress * 0.5));
        
        if (processingStatus === 'completed') {
          processingComplete = true;
        } else if (processingStatus === 'failed') {
          throw new Error('Processing failed');
        } else {
          // Wait before polling again
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
      
      setStatus('completed');
      setProgress(100);
      
      return id;
    } catch (err) {
      setStatus('error');
      setError(err.message || 'An error occurred during processing');
      throw err;
    }
  };
  
  return {
    status,
    progress,
    result,
    error,
    processImage,
  };
}
```

#### 2.3.6 Update Upload Page
**src/app/upload/page.js**
```jsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ImageUploader from '@/components/upload/ImageUploader';
import ImagePreview from '@/components/upload/ImagePreview';
import ProcessingStatus from '@/components/upload/ProcessingStatus';
import { useImageProcessing } from '@/hooks/useImageProcessing';

export default function UploadPage() {
  const router = useRouter();
  const [preview, setPreview] = useState(null);
  const { status, progress, error, processImage } = useImageProcessing();
  
  const handleUpload = async (file, previewUrl) => {
    setPreview(previewUrl);
    
    try {
      const surveyId = await processImage(file);
      
      // Redirect to results page after successful processing
      router.push(`/dashboard?surveyId=${surveyId}`);
    } catch (err) {
      // Error is handled by the hook and displayed in the UI
      console.error('Processing failed:', err);
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Upload Survey Image</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <ImageUploader onUpload={handleUpload} />
        
        {preview && (
          <ImagePreview imageUrl={preview} />
        )}
        
        {status !== 'idle' && (
          <ProcessingStatus status={status} progress={progress} />
        )}
        
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
```

### 2.4 Implement Visualization Components

#### 2.4.1 Create Survey Chart Component
**src/components/visualization/SurveyChart.jsx**
```jsx
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

export default function SurveyChart({ data, type = 'bar' }) {
  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }
  
  return (
    <div className="w-full h-80 mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
```

#### 2.4.2 Create Results Table Component
**src/components/visualization/ResultsTable.jsx**
```jsx
export default function ResultsTable({ data, columns }) {
  if (!data || data.length === 0 || !columns || columns.length === 0) {
    return <div>No data available</div>;
  }
  
  return (
    <div className="mt-4 overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td
                  key={`${rowIndex}-${column.key}`}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

#### 2.4.3 Create Custom Hook for Survey Data
**src/hooks/useSurveyData.js**
```jsx
import { useState, useEffect } from 'react';
import { getSurveyResults } from '../lib/api';

export function useSurveyData(surveyId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!surveyId) {
      setLoading(false);
      return;
    }
    
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getSurveyResults(surveyId);
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to fetch survey data');
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [surveyId]);
  
  return { data, loading, error };
}
```

#### 2.4.4 Update Dashboard Page
**src/app/dashboard/page.js**
```jsx
'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useSurveyData } from '@/hooks/useSurveyData';
import SurveyChart from '@/components/visualization/SurveyChart';
import ResultsTable from '@/components/visualization/ResultsTable';

export default function DashboardPage() {
  const searchParams = useSearchParams();
  const surveyId = searchParams.get('surveyId');
  const { data, loading, error } = useSurveyData(surveyId);
  const [activeView, setActiveView] = useState('charts');
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <p>Loading survey results...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 text-red-700 p-4 rounded-lg">
          {error}
        </div>
      </div>
    );
  }
  
  if (!data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold mb-4">No Survey Selected</h2>
          <p>Please upload a survey or select one from your history.</p>
        </div>
      </div>
    );
  }
  
  // Example data transformation for visualization
  // This would be replaced with actual data from the API
  const chartData = data.questions?.map(q => ({
    name: q.text,
    value: q.responses.filter(r => r === true).length
  })) || [];
  
  const tableColumns = [
    { key: 'question', label: 'Question' },
    { key: 'response', label: 'Response' },
  ];
  
  const tableData = data.questions?.flatMap(q => 
    q.options.map((opt, idx) => ({
      question: q.text,
      response: `Option ${idx + 1}: ${q.responses[idx] ? 'Selected' : 'Not Selected'}`
    }))
  ) || [];
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Survey Results</h1>
        
        <div className="flex gap-4">
          <button
            onClick={() => setActiveView('charts')}
            className={`px-4 py-2 rounded-lg ${
              activeView === 'charts' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}
          >
            Charts
          </button>
          <button
            onClick={() => setActiveView('table')}
            className={`px-4 py-2 rounded-lg ${
              activeView === 'table' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}
          >
            Table
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        {activeView === 'charts' ? (
          <SurveyChart data={chartData} />
        ) : (
          <ResultsTable data={tableData} columns={tableColumns} />
        )}
      </div>
    </div>
  );
}
```

## 3. Backend Implementation

### 3.1 Core Configuration

#### 3.1.1 Create Configuration Settings
**app/core/config.py**
```python
import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Survey OCR API"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./survey_ocr.db")
    
    # File storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    PROCESSED_DIR: str = os.getenv("PROCESSED_DIR", "./processed")
    
    # OCR settings
    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "tesseract")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### 3.1.2 Create Database Session
**app/db/session.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 3.1.3 Create Base Model
**app/db/base.py**
```python
from app.db.session import Base
```

### 3.2 Database Models

#### 3.2.1 Create Survey Model
**app/db/models/survey.py**
```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base

class Survey(Base):
    __tablename__ = "surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_path = Column(String, nullable=False)
    processed_path = Column(String, nullable=True)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    progress = Column(Float, default=0.0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Metadata
    num_questions = Column(Integer, nullable=True)
    num_options = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Survey {self.id}: {self.filename}>"
```

#### 3.2.2 Create Result Model
**app/db/models/result.py**
```python
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    data = Column(JSON, nullable=False)  # Structured survey data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    survey = relationship("Survey", backref="results")
    
    def __repr__(self):
        return f"<Result {self.id} for Survey {self.survey_id}>"
```

#### 3.2.3 Update Models Init File
**app/db/models/__init__.py**
```python
from app.db.models.survey import Survey
from app.db.models.result import Result
```

### 3.3 API Schemas

#### 3.3.1 Create Survey Schemas
**app/schemas/survey.py**
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SurveyBase(BaseModel):
    filename: str
    
class SurveyCreate(SurveyBase):
    pass

class SurveyResponse(BaseModel):
    id: int
    status: str
    progress: float
    message: Optional[str] = None
    
    class Config:
        orm_mode = True

class SurveyStatusResponse(BaseModel):
    id: int
    status: str
    progress: float
    error: Optional[str] = None
    
    class Config:
        orm_mode = True

class SurveyInDB(SurveyBase):
    id: int
    original_path: str
    processed_path: Optional[str] = None
    status: str
    progress: float
    error: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    num_questions: Optional[int] = None
    num_options: Optional[int] = None
    
    class Config:
        orm_mode = True
```

#### 3.3.2 Create Result Schemas
**app/schemas/result.py**
```python
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class ResultBase(BaseModel):
    survey_id: int
    data: Dict[str, Any]

class ResultCreate(ResultBase):
    pass

class ResultResponse(BaseModel):
    survey_id: int
    data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        orm_mode = True

class ResultInDB(ResultBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
```

### 3.4 API Routes

#### 3.4.1 Create Upload Routes
**app/api/routes/upload.py**
```python
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.schemas.survey import SurveyCreate, SurveyResponse
from app.services.ocr.preprocessing import preprocess_image
from app.core.config import settings

router = APIRouter()

@router.post("/upload", response_model=SurveyResponse)
async def upload_survey_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Create survey record
    survey = Survey(
        filename=file.filename,
        original_path=file_path,
        status="uploaded"
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    
    # Start processing in background
    background_tasks.add_task(
        process_survey_image,
        survey_id=survey.id,
        file_path=file_path,
        db=db
    )
    
    return {
        "id": survey.id,
        "status": survey.status,
        "progress": survey.progress,
        "message": "Upload successful, processing started"
    }

async def process_survey_image(survey_id: int, file_path: str, db: Session):
    """Background task to process the uploaded survey image"""
    try:
        # Update status to processing
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "processing"
        survey.progress = 10.0
        db.commit()
        
        # Process image
        await preprocess_image(file_path, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = str(e)
        db.commit()
```

#### 3.4.2 Create Processing Status Routes
**app/api/routes/processing.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.schemas.survey import SurveyStatusResponse

router = APIRouter()

@router.get("/status/{survey_id}", response_model=SurveyStatusResponse)
async def get_processing_status(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return {
        "id": survey.id,
        "status": survey.status,
        "progress": survey.progress,
        "error": survey.error
    }
```

#### 3.4.3 Create Results Routes
**app/api/routes/results.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.db.models.result import Result
from app.schemas.result import ResultResponse

router = APIRouter()

@router.get("/results/{survey_id}", response_model=ResultResponse)
async def get_survey_results(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    if survey.status != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Survey processing not completed. Current status: {survey.status}"
        )
    
    result = db.query(Result).filter(Result.survey_id == survey_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return {
        "survey_id": survey_id,
        "data": result.data,
        "created_at": result.created_at
    }
```

#### 3.4.4 Update Routes Init File
**app/api/routes/__init__.py**
```python
from app.api.routes import upload, processing, results
```

### 3.5 Main Application

#### 3.5.1 Create Main FastAPI Application
**app/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import upload, processing, results
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Survey OCR API",
    description="API for processing survey images using OCR",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(processing.router, prefix="/api", tags=["processing"])
app.include_router(results.router, prefix="/api", tags=["results"])

@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## 4. OCR and Image Processing

### 4.1 Image Preprocessing

#### 4.1.1 Create Preprocessing Module
**app/services/ocr/preprocessing.py**
```python
import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.core.config import settings
from app.services.ocr.bubble_detection import detect_bubbles

async def preprocess_image(file_path: str, survey_id: int, db: Session):
    """Preprocess the survey image for OCR"""
    try:
        # Update progress
        update_progress(survey_id, 20.0, db)
        
        # Read image
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Could not read image at {file_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Create processed directory if it doesn't exist
        os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
        
        # Save preprocessed image
        processed_filename = os.path.basename(file_path)
        processed_path = os.path.join(settings.PROCESSED_DIR, f"preprocessed_{processed_filename}")
        cv2.imwrite(processed_path, thresh)
        
        # Update survey record
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.processed_path = processed_path
        survey.progress = 30.0
        db.commit()
        
        # Continue with bubble detection
        await detect_bubbles(processed_path, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Preprocessing error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
```

### 4.2 Bubble Detection

#### 4.2.1 Create Bubble Detection Module
**app/services/ocr/bubble_detection.py**
```python
import cv2
import numpy as np
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.services.ocr.text_extraction import extract_text

async def detect_bubbles(image_path: str, survey_id: int, db: Session):
    """Detect bubbles/checkboxes in the survey image"""
    try:
        # Update progress
        update_progress(survey_id, 40.0, db)
        
        # Read preprocessed image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find contours
        contours, _ = cv2.findContours(
            gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours to find potential bubbles
        bubbles = []
        for contour in contours:
            # Calculate contour properties
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Filter by area and circularity
            if area > 100 and area < 1000:  # Adjust based on your bubble size
                # Calculate circularity
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Bubbles tend to be circular
                if circularity > 0.7:  # Adjust threshold as needed
                    x, y, w, h = cv2.boundingRect(contour)
                    bubbles.append({
                        "contour": contour,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "area": area,
                        "filled": is_bubble_filled(gray, x, y, w, h)
                    })
        
        # Update progress
        update_progress(survey_id, 60.0, db)
        
        # Continue with text extraction
        await extract_text(image_path, bubbles, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Bubble detection error: {str(e)}"
        db.commit()
        raise

def is_bubble_filled(image, x, y, w, h):
    """Determine if a bubble is filled based on pixel density"""
    # Extract the region of interest
    roi = image[y:y+h, x:x+w]
    
    # Count non-zero pixels (black pixels in the binary image)
    non_zero_count = cv2.countNonZero(roi)
    
    # Calculate the total area
    total_area = w * h
    
    # Calculate the fill ratio
    fill_ratio = non_zero_count / total_area
    
    # If the fill ratio is above a threshold, consider it filled
    return fill_ratio > 0.3  # Adjust threshold as needed

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
```

### 4.3 Text Extraction

#### 4.3.1 Create Text Extraction Module
**app/services/ocr/text_extraction.py**
```python
import cv2
import pytesseract
import numpy as np
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.services.analysis.data_structuring import structure_data

async def extract_text(image_path: str, bubbles, survey_id: int, db: Session):
    """Extract text from the survey image"""
    try:
        # Update progress
        update_progress(survey_id, 70.0, db)
        
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale if not already
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply OCR to the entire image
        text = pytesseract.image_to_string(gray)
        
        # Extract text regions near bubbles
        bubble_text_pairs = []
        
        # Sort bubbles by y-coordinate (top to bottom)
        sorted_bubbles = sorted(bubbles, key=lambda b: b["y"])
        
        # Group bubbles by proximity (likely same question)
        question_groups = group_bubbles_by_question(sorted_bubbles)
        
        # For each question group, extract the question text
        for group in question_groups:
            # Find the region above the first bubble in the group
            first_bubble = group[0]
            question_y = max(0, first_bubble["y"] - 50)  # Look 50 pixels above
            question_height = first_bubble["y"] - question_y
            
            if question_height > 0:
                # Extract question region
                question_region = gray[question_y:first_bubble["y"], :]
                question_text = pytesseract.image_to_string(question_region)
                
                # Add each bubble in the group with the question text
                for bubble in group:
                    bubble_text_pairs.append({
                        "question": question_text.strip(),
                        "x": bubble["x"],
                        "y": bubble["y"],
                        "filled": bubble["filled"]
                    })
        
        # Update progress
        update_progress(survey_id, 80.0, db)
        
        # Continue with data structuring
        await structure_data(bubble_text_pairs, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Text extraction error: {str(e)}"
        db.commit()
        raise

def group_bubbles_by_question(bubbles, vertical_threshold=30):
    """Group bubbles that likely belong to the same question based on vertical proximity"""
    if not bubbles:
        return []
    
    groups = []
    current_group = [bubbles[0]]
    
    for i in range(1, len(bubbles)):
        current_bubble = bubbles[i]
        prev_bubble = bubbles[i-1]
        
        # If this bubble is close vertically to the previous one, add to current group
        if abs(current_bubble["y"] - prev_bubble["y"]) < vertical_threshold:
            current_group.append(current_bubble)
        else:
            # Start a new group
            groups.append(current_group)
            current_group = [current_bubble]
    
    # Add the last group
    if current_group:
        groups.append(current_group)
    
    return groups

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
```

## 5. Data Analysis and Visualization

### 5.1 Data Structuring

#### 5.1.1 Create Data Structuring Module
**app/services/analysis/data_structuring.py**
```python
import json
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.db.models.result import Result
from app.services.analysis.statistics import analyze_results

async def structure_data(bubble_text_pairs, survey_id: int, db: Session):
    """Structure the extracted data into a standardized format"""
    try:
        # Update progress
        update_progress(survey_id, 85.0, db)
        
        # Group by question
        questions = {}
        for pair in bubble_text_pairs:
            question_text = pair["question"]
            if question_text not in questions:
                questions[question_text] = []
            
            questions[question_text].append({
                "x": pair["x"],
                "y": pair["y"],
                "filled": pair["filled"]
            })
        
        # Convert to structured format
        structured_data = {
            "questions": []
        }
        
        for question_text, options in questions.items():
            # Sort options by x-coordinate (left to right)
            sorted_options = sorted(options, key=lambda o: o["x"])
            
            # Create question object
            question = {
                "text": question_text,
                "options": [{"x": opt["x"], "y": opt["y"]} for opt in sorted_options],
                "responses": [opt["filled"] for opt in sorted_options]
            }
            
            structured_data["questions"].append(question)
        
        # Update survey record with metadata
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.num_questions = len(structured_data["questions"])
        survey.num_options = sum(len(q["options"]) for q in structured_data["questions"])
        db.commit()
        
        # Update progress
        update_progress(survey_id, 90.0, db)
        
        # Continue with statistical analysis
        await analyze_results(structured_data, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Data structuring error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
```

### 5.2 Statistical Analysis

#### 5.2.1 Create Statistics Module
**app/services/analysis/statistics.py**
```python
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.db.models.result import Result

async def analyze_results(structured_data, survey_id: int, db: Session):
    """Perform statistical analysis on the structured data"""
    try:
        # Update progress
        update_progress(survey_id, 95.0, db)
        
        # Add statistical analysis to the structured data
        for question in structured_data["questions"]:
            # Calculate response counts
            total_responses = len(question["responses"])
            filled_count = sum(1 for r in question["responses"] if r)
            
            # Add statistics to question
            question["statistics"] = {
                "total_options": total_responses,
                "selected_count": filled_count,
                "percentage": (filled_count / total_responses) * 100 if total_responses > 0 else 0
            }
        
        # Add overall statistics
        total_questions = len(structured_data["questions"])
        total_options = sum(len(q["options"]) for q in structured_data["questions"])
        total_selected = sum(sum(1 for r in q["responses"] if r) for q in structured_data["questions"])
        
        structured_data["statistics"] = {
            "total_questions": total_questions,
            "total_options": total_options,
            "total_selected": total_selected,
            "selection_rate": (total_selected / total_options) * 100 if total_options > 0 else 0
        }
        
        # Save results to database
        result = Result(
            survey_id=survey_id,
            data=structured_data
        )
        db.add(result)
        
        # Update survey status to completed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "completed"
        survey.progress = 100.0
        
        db.commit()
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Statistical analysis error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
```

## 6. Integration and Testing

### 6.1 Start Backend Server

#### 6.1.1 Create Run Script
**backend/run.py**
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 6.2 Start Frontend Development Server

#### 6.2.1 Create Environment File
**frontend/.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 6.3 Testing

#### 6.3.1 Create Test Survey Images
Create or obtain sample survey images with filled bubbles for testing.

#### 6.3.2 Test End-to-End Flow
1. Start the backend server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open a web browser and navigate to http://localhost:3000
4. Upload a test survey image
5. Monitor the processing status
6. View the results in the dashboard

## 7. Deployment

### 7.1 Prepare for Production

#### 7.1.1 Create Docker Files

**backend/Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**frontend/Dockerfile**
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build

CMD ["npm", "start"]
```

#### 7.1.2 Create Docker Compose File
**docker-compose.yml**
```yaml
version: '3'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
      - ./processed:/app/processed
    environment:
      - DATABASE_URL=sqlite:///./survey_ocr.db
      - UPLOAD_DIR=./uploads
      - PROCESSED_DIR=./processed
      - TESSERACT_CMD=tesseract

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api
    depends_on:
      - backend
```

### 7.2 Deploy to Production

#### 7.2.1 Build and Start Docker Containers
```bash
docker-compose up -d --build
```

#### 7.2.2 Access the Application
Open a web browser and navigate to http://localhost:3000

## Conclusion

This step-by-step guide provides detailed instructions for implementing the Survey OCR project from start to finish. By following these steps, you can create a web application that allows users to upload images of surveys with filled dots/bubbles, processes them using OCR and computer vision, and generates visualizations of the results.

The guide covers all aspects of the project, including:
- Setting up the development environment
- Implementing the frontend with Next.js and React
- Implementing the backend with FastAPI
- Creating OCR and image processing components
- Developing data analysis and visualization features
- Testing and deploying the application

By breaking down the implementation into manageable steps, this guide makes it easier to understand and implement the Survey OCR project.
