import { PredictionRequest, PredictionResponse } from '../types/prediction';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function predictHousePrice(data: PredictionRequest): Promise<PredictionResponse> {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch prediction from the server');
  }

  return response.json();
}
