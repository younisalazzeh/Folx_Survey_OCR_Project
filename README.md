# Survey OCR Project Documentation

## Project Overview

The Survey OCR (Optical Character Recognition) project is a full-stack web application designed to automate the processing of survey forms. The application allows users to upload images of completed surveys, processes them using OCR technology to detect filled bubbles and extract text, and presents the results in an interactive dashboard with visualizations.

## Architecture

The project follows a client-server architecture with:

1. **Backend**: A FastAPI application that handles image processing, OCR, and data storage
2. **Frontend**: A Next.js application that provides the user interface for uploading images and viewing results

## Key Features

- Image upload with drag-and-drop functionality
- Automated survey processing with OCR
- Real-time processing status updates
- Interactive data visualization
- Responsive design for desktop and mobile devices

## Technical Implementation

### Backend Components

- **FastAPI Framework**: Provides the REST API endpoints
- **SQLAlchemy ORM**: Handles database operations
- **OpenCV**: Performs image preprocessing and bubble detection
- **Tesseract OCR**: Extracts text from images
- **Pydantic**: Handles data validation and serialization

### Frontend Components

- **Next.js**: React framework for building the user interface
- **React Hooks**: Manages component state and side effects
- **React Dropzone**: Handles file uploads
- **Recharts**: Creates interactive data visualizations
- **Tailwind CSS**: Styles the application

### Database Schema

The application uses SQLite with two main tables:

1. **Surveys**: Stores metadata about uploaded surveys
   - ID, filename, paths, status, progress, error messages, timestamps

2. **Results**: Stores processed survey data
   - Survey ID, structured JSON data, timestamps

### OCR Pipeline

The OCR processing pipeline consists of several stages:

1. **Preprocessing**: Converts the image to grayscale, applies blur and thresholding
2. **Bubble Detection**: Identifies potential bubbles based on shape and size
3. **Text Extraction**: Uses Tesseract OCR to extract question text
4. **Data Structuring**: Organizes detected bubbles and text into a structured format
5. **Statistical Analysis**: Calculates response rates and other metrics

## Running the Application

### Prerequisites

- Python 3.10+
- Node.js and npm/pnpm
- Tesseract OCR

### Backend Setup

```bash
cd survey_ocr_project/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pydantic-settings
mkdir -p uploads processed
python main.py
```

### Frontend Setup

```bash
cd survey_ocr_project/frontend
pnpm install  # or npm install
# Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000/api
pnpm dev  # or npm run dev
```

## Usage Guide

1. Navigate to http://localhost:3000
2. Click "Upload Survey"
3. Drag and drop a survey image or click to select one
4. Wait for processing to complete
5. View results in the dashboard

## Testing

The application includes test survey images in the `test_images` directory:
- `blank_survey.png`: An empty survey form
- `filled_survey.png`: A survey with some bubbles filled in

These can be used to test the OCR functionality without creating real survey forms.

## Future Enhancements

- User authentication and authorization
- Support for multiple survey templates
- Batch processing of multiple surveys
- Export functionality for results
- Advanced analytics and reporting
