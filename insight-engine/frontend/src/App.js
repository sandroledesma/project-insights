import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import CategorySlider from './components/CategorySlider';
import AIToolList from './pages/AIToolList';
import LuxeApplianceList from './pages/LuxeApplianceList';
import ComparisonPage from './pages/ComparisonPage';
import ComingSoonPage from './pages/ComingSoonPage';
import './App.css';

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="App bg-gray-100 dark:bg-dark-bg min-h-screen">
        <Header />
        <CategorySlider />
        <main className="bg-gray-100 dark:bg-dark-bg">
          <Routes>
            {/* Technology */}
            <Route path="/" element={<AIToolList />} />
            <Route path="/productivity" element={<ComingSoonPage />} />
            <Route path="/creative" element={<ComingSoonPage />} />
            
            {/* Appliances */}
            <Route path="/kitchen" element={<ComingSoonPage />} />
            <Route path="/laundry" element={<ComingSoonPage />} />
            <Route path="/small-appliances" element={<ComingSoonPage />} />
            <Route path="/luxe" element={<LuxeApplianceList />} />
            
            {/* Music */}
            <Route path="/guitars" element={<ComingSoonPage />} />
            <Route path="/keyboards" element={<ComingSoonPage />} />
            <Route path="/turntables" element={<ComingSoonPage />} />
            <Route path="/audio-gear" element={<ComingSoonPage />} />
            
            {/* Transport */}
            <Route path="/scooters" element={<ComingSoonPage />} />
            <Route path="/skateboards" element={<ComingSoonPage />} />
            <Route path="/bikes" element={<ComingSoonPage />} />
            <Route path="/cars" element={<ComingSoonPage />} />
            
            {/* Gaming */}
            <Route path="/gaming-pc" element={<ComingSoonPage />} />
            <Route path="/consoles" element={<ComingSoonPage />} />
            <Route path="/peripherals" element={<ComingSoonPage />} />
            <Route path="/mobile-gaming" element={<ComingSoonPage />} />
            
            {/* Fitness */}
            <Route path="/home-gym" element={<ComingSoonPage />} />
            <Route path="/wearables" element={<ComingSoonPage />} />
            <Route path="/supplements" element={<ComingSoonPage />} />
            <Route path="/outdoor" element={<ComingSoonPage />} />
            
            {/* Compare */}
            <Route path="/compare" element={<ComparisonPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 