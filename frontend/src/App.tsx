import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultPage from './pages/ResultPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <Router>
      <div style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/result" element={<ResultPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
