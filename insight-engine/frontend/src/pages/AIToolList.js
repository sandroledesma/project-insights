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

  // Filter tools based on search term and filters
  const filteredTools = tools.filter(tool => {
    const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tool.short_description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesUseCase = !filterUseCase || tool.primary_use_case === filterUseCase;
    const matchesPricing = !filterPricing || tool.pricing_model === filterPricing;
    
    return matchesSearch && matchesUseCase && matchesPricing;
  });

  // Get unique values for filters
  const useCases = [...new Set(tools.map(tool => tool.primary_use_case).filter(Boolean))];
  const pricingModels = [...new Set(tools.map(tool => tool.pricing_model).filter(Boolean))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={fetchTools}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Platforms</h1>
        <p className="text-gray-600">Discover and compare the best AI tools and platforms</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              id="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search tools..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Use Case Filter */}
          <div>
            <label htmlFor="useCase" className="block text-sm font-medium text-gray-700 mb-1">
              Use Case
            </label>
            <select
              id="useCase"
              value={filterUseCase}
              onChange={(e) => setFilterUseCase(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">All Use Cases</option>
              {useCases.map(useCase => (
                <option key={useCase} value={useCase}>{useCase}</option>
              ))}
            </select>
          </div>

          {/* Pricing Filter */}
          <div>
            <label htmlFor="pricing" className="block text-sm font-medium text-gray-700 mb-1">
              Pricing Model
            </label>
            <select
              id="pricing"
              value={filterPricing}
              onChange={(e) => setFilterPricing(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">All Pricing Models</option>
              {pricingModels.map(pricing => (
                <option key={pricing} value={pricing}>{pricing}</option>
              ))}
            </select>
          </div>

          {/* Results Count */}
          <div className="flex items-end">
            <span className="text-sm text-gray-600">
              {filteredTools.length} of {tools.length} tools
            </span>
          </div>
        </div>
      </div>

      {/* Tools Grid */}
      {filteredTools.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg mb-2">No tools found</div>
          <p className="text-gray-400">Try adjusting your search or filters</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTools.map(tool => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AIToolList; 