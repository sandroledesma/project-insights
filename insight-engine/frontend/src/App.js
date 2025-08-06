import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import AIToolList from './pages/AIToolList';
import LuxeApplianceList from './pages/LuxeApplianceList';
import ComparisonPage from './pages/ComparisonPage';
import './App.css';

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<AIToolList />} />
            <Route path="/luxe" element={<LuxeApplianceList />} />
            <Route path="/compare" element={<ComparisonPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 