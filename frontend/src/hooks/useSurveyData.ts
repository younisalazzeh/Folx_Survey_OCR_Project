import { useState, useEffect } from 'react';

export function useSurveyData(surveyId: number | null) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (!surveyId) {
      return;
    }
    
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Import dynamically to avoid server-side issues
        const { getSurveyResults } = await import('@/lib/api');
        
        const response = await getSurveyResults(surveyId);
        setData(response.data);
        setError(null);
      } catch (err: any) {
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
