# Survey OCR Project Documentation

## Project Overview

The Survey OCR (Optical Character Recognition) project is a full-stack web application designed to automate the processing of survey forms. The application allows users to upload images of completed surveys, processes them using OCR technology to detect filled bubbles and extract text, and presents the results in an interactive dashboard with visualizations.

## Repository Structure

```
/
├── backend/         # FastAPI backend code (Python)
├── frontend/        # Next.js frontend code (TypeScript/React)
│   ├── src/
│   │   ├── app/       # Next.js pages
│   │   ├── components/  # Reusable React components
│   │   ├── hooks/     # Custom React hooks
│   │   └── lib/       # Utility functions
├── docs/            # Documentation files
│   └── images/      # Image assets for documentation/testing
├── scripts/         # Utility scripts (e.g., test image generation)
├── .env.example     # Example environment variables
├── .gitignore       # Git ignore file
└── README.md        # This file
```

## Architecture

The project follows a client-server architecture with:

1.  **Backend**: A FastAPI application located in the `backend/` directory that handles image processing, OCR, and data storage.
2.  **Frontend**: A Next.js application located in the `frontend/` directory that provides the user interface for uploading images and viewing results.

## Key Features

- Image upload with drag-and-drop functionality
- Automated survey processing with OCR
- Real-time processing status updates
- Interactive data visualization
- Responsive design for desktop and mobile devices

## Technical Implementation

### Backend Components (`backend/`)

- **FastAPI Framework**: Provides the REST API endpoints
- **SQLAlchemy ORM**: Handles database operations
- **OpenCV**: Performs image preprocessing and bubble detection
- **Tesseract OCR**: Extracts text from images
- **Pydantic**: Handles data validation and serialization

### Frontend Components (`frontend/`)

- **Next.js**: React framework for building the user interface
- **React Hooks**: Manages component state and side effects
- **React Dropzone**: Handles file uploads
- **Recharts**: Creates interactive data visualizations
- **Tailwind CSS**: Styles the application

### Database Schema

The application uses SQLite with two main tables:

1.  **Surveys**: Stores metadata about uploaded surveys
    - ID, filename, paths, status, progress, error messages, timestamps

2.  **Results**: Stores processed survey data
    - Survey ID, structured JSON data, timestamps

### OCR Pipeline

The OCR processing pipeline consists of several stages:

1.  **Preprocessing**: Converts the image to grayscale, applies blur and thresholding
2.  **Bubble Detection**: Identifies potential bubbles based on shape and size
3.  **Text Extraction**: Uses Tesseract OCR to extract question text
4.  **Data Structuring**: Organizes detected bubbles and text into a structured format
5.  **Statistical Analysis**: Calculates response rates and other metrics

## Running the Application

### Prerequisites

- Python 3.10+
- Node.js and npm/pnpm
- Tesseract OCR

### Environment Setup

1.  Copy the `.env.example` file to `.env.local` in the root directory.
    ```bash
    cp .env.example .env.local
    ```
2.  Update `.env.local` if your backend API runs on a different URL.

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt # Assuming requirements.txt exists or needs to be generated
pip install pydantic-settings fastapi uvicorn[standard] python-multipart opencv-python-headless Pillow python-dotenv SQLAlchemy alembic psycopg2-binary # Add other necessary backend dependencies
mkdir -p uploads processed # These should likely be gitignored
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*Note: A `requirements.txt` file is recommended for the backend. You might need to generate it using `pip freeze > requirements.txt` after installing dependencies.* 
*Note: The `uploads` and `processed` directories are created for runtime use and should typically be included in `.gitignore`.* 

### Frontend Setup

```bash
cd frontend
pnpm install  # or npm install
pnpm dev      # or npm run dev
```

## Usage Guide

1.  Ensure both backend and frontend servers are running.
2.  Navigate to http://localhost:3000 (or your frontend's URL).
3.  Click "Upload Survey".
4.  Drag and drop a survey image or click to select one.
5.  Wait for processing to complete.
6.  View results in the dashboard.

## Testing

The application includes a test survey image in the `docs/images/` directory:
- `filled_survey.png`: A survey with some bubbles filled in.

You can use this image to test the OCR functionality.
The `scripts/create_test_images.py` script can be used to generate more test data if needed.

## Future Enhancements

- User authentication and authorization
- Support for multiple survey templates
- Batch processing of multiple surveys
- Export functionality for results
- Advanced analytics and reporting
- Add backend `requirements.txt`
- Add frontend `package.json` if missing

