import { useState } from 'react';

export function useImageProcessing() {
  const [status, setStatus] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  
  const processImage = async (file: File) => {
    try {
      // Update status to uploading
      setStatus('uploading');
      setProgress(10);
      setError(null);
      
      // Import dynamically to avoid server-side issues
      const { uploadSurveyImage, getProcessingStatus } = await import('@/lib/api');
      
      // Upload the image
      const uploadResponse = await uploadSurveyImage(file);
      const { id } = uploadResponse;
      
      // Poll for processing status
      setStatus('processing');
      let processingComplete = false;
      
      while (!processingComplete) {
        const statusResponse = await getProcessingStatus(id);
        const { status: processingStatus, progress: processingProgress } = statusResponse;
        
        setProgress(Math.min(95, processingProgress));
        
        if (processingStatus === 'completed') {
          processingComplete = true;
          setStatus('completed');
          setProgress(100);
        } else if (processingStatus === 'failed') {
          throw new Error(statusResponse.error || 'Processing failed');
        } else {
          // Wait before polling again
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
      
      return id;
    } catch (err: any) {
      setStatus('error');
      setError(err.message || 'An error occurred during processing');
      throw err;
    }
  };
  
  return {
    status,
    progress,
    error,
    processImage,
  };
}
