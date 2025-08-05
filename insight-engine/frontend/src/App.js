import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AIToolList from './pages/AIToolList';
import ComparisonPage from './pages/ComparisonPage';
import Header from './components/Header';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<AIToolList />} />
            <Route path="/compare" element={<ComparisonPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 