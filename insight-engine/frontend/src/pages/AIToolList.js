import React, { useState, useEffect } from 'react';
import ToolCard from '../components/ToolCard';
import apiService from '../services/api';

const AIToolList = () => {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterUseCase, setFilterUseCase] = useState('');
  const [filterPricing, setFilterPricing] = useState('');
  const [sortBy, setSortBy] = useState('rating'); // Default to rating sort

  useEffect(() => {
    fetchTools();
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">AI Tool Reviews</h1>
            <p className="text-lg text-gray-600">Discover and compare AI tools based on real Reddit reviews</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <div className="lg:w-80 flex-shrink-0">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Filters</h2>
              
              {/* Search */}
              <div className="mb-6">
                <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                  Search Tools
                </label>
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search by name or description..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Sort By */}
              <div className="mb-6">
                <label htmlFor="sortBy" className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  id="sortBy"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="rating">Rating (Highest First)</option>
                  <option value="name">Name (A-Z)</option>
                  <option value="reviews">Has Reviews</option>
                </select>
              </div>

              {/* Use Case Filter */}
              <div className="mb-6">
                <label htmlFor="useCase" className="block text-sm font-medium text-gray-700 mb-2">
                  Use Case
                </label>
                <select
                  id="useCase"
                  value={filterUseCase}
                  onChange={(e) => setFilterUseCase(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Use Cases</option>
                  {useCases.map(useCase => (
                    <option key={useCase} value={useCase}>{useCase}</option>
                  ))}
                </select>
              </div>

              {/* Pricing Filter */}
              <div className="mb-6">
                <label htmlFor="pricing" className="block text-sm font-medium text-gray-700 mb-2">
                  Pricing Model
                </label>
                <select
                  id="pricing"
                  value={filterPricing}
                  onChange={(e) => setFilterPricing(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Pricing Models</option>
                  {pricingModels.map(pricing => (
                    <option key={pricing} value={pricing}>{pricing}</option>
                  ))}
                </select>
              </div>

              {/* Results Count */}
              <div className="pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  Showing {filteredAndSortedTools.length} of {tools.length} tools
                </p>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Tools Grid */}
            {filteredAndSortedTools.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg mb-2">No tools found</div>
                <p className="text-gray-400">Try adjusting your search or filters</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredAndSortedTools.map(tool => (
                  <ToolCard key={tool.id} tool={tool} onRefresh={handleRefreshAllTools} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIToolList; 