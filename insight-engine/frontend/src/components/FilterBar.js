import React, { useState, useEffect } from 'react';

const FilterBar = ({ 
  searchTerm, 
  setSearchTerm, 
  sortBy, 
  setSortBy, 
  filters = [],
  sortOptions = [],
  resultsCount,
  totalCount,
  placeholder = "Search..."
}) => {
  const [showFilters, setShowFilters] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const [isScrolled, setIsScrolled] = useState(false);

  // Handle scroll events for responsive behavior
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      setScrollY(currentScrollY);
      setIsScrolled(currentScrollY > 100);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Calculate dynamic values based on scroll - tighter spacing
  const dynamicTop = Math.max(16, 80 - scrollY / 5); // Reduced from 112 to 80
  const containerPadding = Math.max(6, 12 - scrollY / 20); // Reduced from 8-16 to 6-12
  const fontSize = Math.max(12, 14 - scrollY / 100);

  return (
    <div 
      className={`bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700 sticky z-30 shadow-sm transition-all duration-300 ${
        isScrolled ? 'backdrop-blur-md bg-white/95 dark:bg-dark-card/95' : ''
      }`}
      style={{ top: `${dynamicTop}px` }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div 
          className="transition-all duration-300"
          style={{ paddingTop: `${containerPadding}px`, paddingBottom: `${containerPadding}px` }}
        >
          {/* Main Filter Row */}
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            {/* Search Bar */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder={placeholder}
                  className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent-green focus:border-transparent transition-colors"
                />
              </div>
            </div>

            {/* Sort Dropdown */}
            <div className="flex items-center space-x-3">
              <label 
                className="font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap transition-all duration-300"
                style={{ fontSize: `${fontSize}px` }}
              >
                Sort by:
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-accent-green focus:border-transparent transition-colors"
              >
                {sortOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>

            {/* Filters Toggle */}
            {filters.length > 0 && (
              <button
                onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg border transition-colors ${
                  showFilters 
                    ? 'bg-accent-green/10 border-accent-green text-accent-green' 
                    : 'bg-gray-50 dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.707A1 1 0 013 7V4z" />
                </svg>
                <span 
                  className="font-medium transition-all duration-300"
                  style={{ fontSize: `${fontSize}px` }}
                >
                  Filters
                </span>
                {showFilters ? (
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                  </svg>
                ) : (
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                )}
              </button>
            )}

            {/* Results Count */}
            <div 
              className="text-gray-500 dark:text-gray-400 whitespace-nowrap transition-all duration-300"
              style={{ fontSize: `${Math.max(10, fontSize - 1)}px` }}
            >
              {resultsCount} of {totalCount} results
            </div>
          </div>

          {/* Expandable Filters Section */}
          {showFilters && filters.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filters.map((filter, index) => (
                  <div key={index} className="space-y-1">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      {filter.label}
                    </label>
                    <select
                      value={filter.value}
                      onChange={(e) => filter.onChange(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-accent-green focus:border-transparent transition-colors text-sm"
                    >
                      <option value="">{filter.allLabel || `All ${filter.label}`}</option>
                      {filter.options.map(option => (
                        <option key={option} value={option}>{option}</option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FilterBar;