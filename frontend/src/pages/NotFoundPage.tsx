import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div style={{ padding: '4rem 2rem', textAlign: 'center' }}>
      <h1 style={{ fontSize: '4rem', color: '#dc3545', margin: 0 }}>404</h1>
      <h2 style={{ margin: '1rem 0' }}>Page Not Found</h2>
      <p style={{ color: '#666', marginBottom: '2rem' }}>The page you are looking for does not exist.</p>
      <Link to="/" style={{ padding: '0.8rem 1.5rem', backgroundColor: '#007BFF', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>
        Go back home
      </Link>
    </div>
  );
}
