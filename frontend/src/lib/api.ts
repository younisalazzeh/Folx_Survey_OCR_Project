// API client for communicating with the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function uploadSurveyImage(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }
  
  return response.json();
}

export async function getProcessingStatus(surveyId: number) {
  const response = await fetch(`${API_BASE_URL}/status/${surveyId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get status: ${response.statusText}`);
  }
  
  return response.json();
}

export async function getSurveyResults(surveyId: number) {
  const response = await fetch(`${API_BASE_URL}/results/${surveyId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get results: ${response.statusText}`);
  }
  
  return response.json();
}
