import { useLocation, Link, Navigate } from 'react-router-dom';

export default function ResultPage() {
  const location = useLocation();
  const state = location.state as { price: number; formData: any } | null;

  if (!state) {
    return <Navigate to="/" replace />;
  }

  const formatPrice = (price: number) => {
    if (price >= 10000000) {
      return `₹ ${(price / 10000000).toFixed(2)} Cr`;
    } else if (price >= 100000) {
      return `₹ ${(price / 100000).toFixed(2)} Lac`;
    }
    return `₹ ${price.toLocaleString('en-IN')}`;
  };

  return (
    <div style={{ padding: '2rem', textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ color: '#333' }}>Prediction Result</h1>
      <div style={{ margin: '2rem 0', padding: '2rem', backgroundColor: '#f0f8ff', borderRadius: '8px', border: '1px solid #cce5ff' }}>
        <h2 style={{ margin: 0, color: '#555' }}>Estimated Price</h2>
        <h1 style={{ color: '#007BFF', fontSize: '3rem', margin: '1rem 0' }}>{formatPrice(state.price)}</h1>
      </div>
      
      <div style={{ marginBottom: '2rem', textAlign: 'left', backgroundColor: '#f9f9f9', padding: '1.5rem', borderRadius: '8px' }}>
        <h3 style={{ marginTop: 0 }}>Property Details:</h3>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
          <li><strong>Location:</strong> {state.formData.location}</li>
          <li><strong>Area:</strong> {state.formData.area_sqft} sqft</li>
          <li><strong>Floor:</strong> {state.formData.floor_num}</li>
          <li><strong>Bathrooms:</strong> {state.formData.bathroom}</li>
          <li><strong>Furnishing:</strong> {state.formData.furnishing}</li>
          <li><strong>Status:</strong> {state.formData.status}</li>
        </ul>
      </div>

      <Link to="/" style={{ display: 'inline-block', padding: '0.8rem 1.5rem', backgroundColor: '#6c757d', color: 'white', textDecoration: 'none', borderRadius: '4px', fontWeight: 'bold' }}>
        Make Another Prediction
      </Link>
    </div>
  );
}
