import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import locations from '../data/locations.json';
import { PredictionRequest } from '../types/prediction';
import { predictHousePrice } from '../api/predictionClient';

export default function PredictionForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState<PredictionRequest>({
    location: locations[0] || 'other',
    area_sqft: 0,
    floor_num: 0,
    bathroom: 1,
    balcony: 0,
    parking: 0,
    furnishing: 'Unfurnished',
    transaction: 'Resale',
    ownership: 'Freehold',
    facing: 'East',
    status: 'Ready to Move'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (formData.area_sqft <= 0) {
      setError('Area must be greater than 0');
      return;
    }

    setLoading(true);
    try {
      const result = await predictHousePrice(formData);
      navigate('/result', { state: { price: result.predicted_price, formData } });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '500px', margin: '0 auto' }}>
      {error && <div style={{ color: 'red', padding: '0.5rem', border: '1px solid red' }}>{error}</div>}
      
      <div>
        <label>Location:</label>
        <select name="location" value={formData.location} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
        </select>
      </div>

      <div>
        <label>Carpet Area (sqft):</label>
        <input type="number" name="area_sqft" value={formData.area_sqft || ''} onChange={handleChange} required min="1" style={{width: '100%', padding: '0.5rem'}} />
      </div>

      <div>
        <label>Floor Number:</label>
        <input type="number" name="floor_num" value={formData.floor_num} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}} />
      </div>

      <div>
        <label>Bathrooms:</label>
        <input type="number" name="bathroom" value={formData.bathroom} onChange={handleChange} required min="1" style={{width: '100%', padding: '0.5rem'}} />
      </div>

      <div>
        <label>Balconies:</label>
        <input type="number" name="balcony" value={formData.balcony} onChange={handleChange} required min="0" style={{width: '100%', padding: '0.5rem'}} />
      </div>

      <div>
        <label>Parking Spaces:</label>
        <input type="number" name="parking" value={formData.parking} onChange={handleChange} required min="0" style={{width: '100%', padding: '0.5rem'}} />
      </div>

      <div>
        <label>Furnishing:</label>
        <select name="furnishing" value={formData.furnishing} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          <option value="Furnished">Furnished</option>
          <option value="Semi-Furnished">Semi-Furnished</option>
          <option value="Unfurnished">Unfurnished</option>
        </select>
      </div>

      <div>
        <label>Transaction Type:</label>
        <select name="transaction" value={formData.transaction} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          <option value="New Property">New Property</option>
          <option value="Resale">Resale</option>
        </select>
      </div>

      <div>
        <label>Ownership:</label>
        <select name="ownership" value={formData.ownership} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          <option value="Freehold">Freehold</option>
          <option value="Leasehold">Leasehold</option>
          <option value="Co-operative Society">Co-operative Society</option>
          <option value="Power of Attorney">Power of Attorney</option>
        </select>
      </div>

      <div>
        <label>Facing:</label>
        <select name="facing" value={formData.facing} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          <option value="East">East</option>
          <option value="West">West</option>
          <option value="North">North</option>
          <option value="South">South</option>
          <option value="North-East">North-East</option>
          <option value="North-West">North-West</option>
          <option value="South-East">South-East</option>
          <option value="South-West">South-West</option>
        </select>
      </div>

      <div>
        <label>Status:</label>
        <select name="status" value={formData.status} onChange={handleChange} required style={{width: '100%', padding: '0.5rem'}}>
          <option value="Ready to Move">Ready to Move</option>
          <option value="Under Construction">Under Construction</option>
        </select>
      </div>

      <button type="submit" disabled={loading} style={{ padding: '0.8rem', backgroundColor: '#007BFF', color: 'white', border: 'none', cursor: 'pointer', marginTop: '1rem', fontSize: '1rem', borderRadius: '4px' }}>
        {loading ? 'Predicting...' : 'Get Price Prediction'}
      </button>
    </form>
  );
}
