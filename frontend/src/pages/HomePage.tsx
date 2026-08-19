import PredictionForm from '../components/PredictionForm';

export default function HomePage() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>🏠 House Price Predictor</h1>
      <p style={{ textAlign: 'center', marginBottom: '2rem', color: '#666' }}>
        Enter the property details below to get an estimated price based on our machine learning model.
      </p>
      <PredictionForm />
    </div>
  );
}
