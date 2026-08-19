export interface PredictionRequest {
  location: string;
  area_sqft: number;
  floor_num: number;
  bathroom: number;
  balcony: number;
  parking: number;
  furnishing: string;
  transaction: string;
  ownership: string;
  facing: string;
  status: string;
}

export interface PredictionResponse {
  predicted_price: number;
}
