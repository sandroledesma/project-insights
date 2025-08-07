import React, { useState, useEffect } from 'react';
import ToolCard from '../components/ToolCard';
import FilterBar from '../components/FilterBar';
import apiService from '../services/api';

const AIToolList = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUseCase, setFilterUseCase] = useState('');
  const [filterPricing, setFilterPricing] = useState('');
  const [sortBy, setSortBy] = useState('rating'); // Default to rating sort
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    fetchTools();
  }, []);

  // Handle scroll events for responsive header
  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const fetchTools = async () => {
    try {
      setLoading(true);
      const toolsData = await apiService.getAITools();
      setTools(toolsData);
      setError(null);
    } catch (err) {
      setError('Failed to load AI tools. Please try again later.');
      console.error('Error fetching tools:', err);
    } finally {
      setLoading(false);
    }
  };

  // Filter and sort tools
  const filteredAndSortedTools = tools
    .filter(tool => {
      const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           tool.short_description?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesUseCase = !filterUseCase || tool.primary_use_case === filterUseCase;
      const matchesPricing = !filterPricing || tool.pricing_model === filterPricing;
      
      return matchesSearch && matchesUseCase && matchesPricing;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'rating':
          const ratingA = a.aggregated_review?.overall_rating || 0;
          const ratingB = b.aggregated_review?.overall_rating || 0;
          return ratingB - ratingA; // Highest first
        case 'reviews':
          const reviewsA = a.aggregated_review ? 1 : 0;
          const reviewsB = b.aggregated_review ? 1 : 0;
          return reviewsB - reviewsA; // Has reviews first
        case 'name':
        default:
          return a.name.localeCompare(b.name);
      }
    });

  // Get unique values for filters
  const useCases = [...new Set(tools.map(tool => tool.primary_use_case).filter(Boolean))];
  const pricingModels = [...new Set(tools.map(tool => tool.pricing_model).filter(Boolean))];

  // Enhanced refresh function that reloads all tools
  const handleRefreshAllTools = async () => {
    console.log('Refreshing all tools data...');
    await fetchTools();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading AI tools...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={fetchTools}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Define filter options for the FilterBar component
  const sortOptions = [
    { value: 'rating', label: 'Rating (Highest First)' },
    { value: 'name', label: 'Name (A-Z)' },
    { value: 'reviews', label: 'Has Reviews' }
  ];

  const filters = [
    {
      label: 'Use Case',
      value: filterUseCase,
      onChange: setFilterUseCase,
      options: useCases,
      allLabel: 'All Use Cases'
    },
    {
      label: 'Pricing Model',
      value: filterPricing,
      onChange: setFilterPricing,
      options: pricingModels,
      allLabel: 'All Pricing Models'
    }
  ];

  // Calculate dynamic values based on scroll - tighter spacing
  const headerPadding = Math.max(12, 24 - scrollY / 10); // Reduced from 16-32 to 12-24
  const iconSize = Math.max(28, 48 - scrollY / 5); // Reduced from 32-64 to 28-48
  const titleSize = Math.max(18, 28 - scrollY / 8); // Reduced from 20-36 to 18-28
  const subtitleSize = Math.max(13, 16 - scrollY / 15); // Reduced from 14-18 to 13-16
  const subtitleOpacity = Math.max(0, 1 - scrollY / 150);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-dark-bg">
      {/* Header with scroll-responsive behavior */}
      <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div 
            className="transition-all duration-300"
            style={{ paddingTop: `${headerPadding}px`, paddingBottom: `${headerPadding}px` }}
          >
            <div className="text-center">
              <div 
                className="inline-flex items-center justify-center rounded-xl mb-4 bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-lg transition-all duration-300"
                style={{ 
                  width: `${iconSize}px`, 
                  height: `${iconSize}px`,
                  marginBottom: `${Math.max(6, 12 - scrollY / 20)}px` // Reduced from 8-16 to 6-12
                }}
              >
                <svg 
                  className="transition-all duration-300" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  style={{ width: `${iconSize * 0.5}px`, height: `${iconSize * 0.5}px` }}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h1 
                className="font-bold text-gray-800 dark:text-white mb-2 transition-all duration-300"
                style={{ 
                  fontSize: `${titleSize}px`,
                  marginBottom: `${Math.max(3, 6 - scrollY / 40)}px` // Reduced from 4-8 to 3-6
                }}
              >
                AI Tools
              </h1>
              <p 
                className="text-gray-500 dark:text-gray-400 transition-all duration-300"
                style={{ 
                  fontSize: `${subtitleSize}px`,
                  opacity: subtitleOpacity,
                  transform: `translateY(${(1 - subtitleOpacity) * -10}px)`
                }}
              >
                Discover and compare AI tools based on real Reddit reviews
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <FilterBar
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        sortBy={sortBy}
        setSortBy={setSortBy}
        filters={filters}
        sortOptions={sortOptions}
        resultsCount={filteredAndSortedTools.length}
        totalCount={tools.length}
        placeholder="Search by name or description..."
      />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredAndSortedTools.length === 0 ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div className="text-gray-500 dark:text-gray-400 text-lg mb-2">No tools found</div>
            <p className="text-gray-400 dark:text-gray-500">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-8">
            {filteredAndSortedTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} onRefresh={handleRefreshAllTools} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AIToolList; 