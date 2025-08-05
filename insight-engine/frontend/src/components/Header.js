import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">IE</span>
            </div>
            <div>
              <span className="text-xl font-bold text-gray-900">Insight-Engine</span>
              <span className="block text-xs text-gray-500">Review Analytics</span>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/')
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              AI Tools
            </Link>
            <Link
              to="/luxe"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/luxe')
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              Luxe Appliances
            </Link>
            <Link
              to="/compare"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/compare')
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              Compare
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 