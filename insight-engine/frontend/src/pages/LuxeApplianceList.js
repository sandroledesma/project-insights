import React, { useState, useEffect } from 'react';
import LuxeApplianceCard from '../components/LuxeApplianceCard';
import apiService from '../services/api';

const LuxeApplianceList = () => {
  const [appliances, setAppliances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterBrand, setFilterBrand] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterDesignStyle, setFilterDesignStyle] = useState('');
  const [sortBy, setSortBy] = useState('rating'); // Default to rating sort
  const [designInsights, setDesignInsights] = useState(null);

  useEffect(() => {
    fetchAppliances();
    fetchDesignInsights();
  }, []);

  const fetchAppliances = async () => {
    try {
      setLoading(true);
      const appliancesData = await apiService.getLuxeAppliances();
      setAppliances(appliancesData);
      setError(null);
    } catch (err) {
      setError('Failed to load luxury appliances. Please try again later.');
      console.error('Error fetching appliances:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDesignInsights = async () => {
    try {
      const insights = await apiService.getDesignInsights();
      setDesignInsights(insights);
    } catch (err) {
      console.error('Error fetching design insights:', err);
    }
  };

  // Filter and sort appliances
  const filteredAndSortedAppliances = appliances
    .filter(appliance => {
      const matchesSearch = appliance.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           appliance.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           appliance.brand.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesBrand = !filterBrand || appliance.brand === filterBrand;
      const matchesCategory = !filterCategory || appliance.category === filterCategory;
      const matchesDesignStyle = !filterDesignStyle || appliance.design_style === filterDesignStyle;
      
      return matchesSearch && matchesBrand && matchesCategory && matchesDesignStyle;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'rating':
          const ratingA = a.aggregated_review?.overall_rating || 0;
          const ratingB = b.aggregated_review?.overall_rating || 0;
          return ratingB - ratingA; // Highest first
        case 'design_rating':
          const designRatingA = a.aggregated_review?.design_rating || 0;
          const designRatingB = b.aggregated_review?.design_rating || 0;
          return designRatingB - designRatingA;
        case 'price':
          const priceA = parseFloat(a.price_range?.replace(/[^0-9]/g, '') || '0');
          const priceB = parseFloat(b.price_range?.replace(/[^0-9]/g, '') || '0');
          return priceB - priceA; // Highest price first
        case 'brand':
          return a.brand.localeCompare(b.brand);
        case 'name':
        default:
          return a.name.localeCompare(b.name);
      }
    });

  // Get unique values for filters
  const brands = [...new Set(appliances.map(appliance => appliance.brand).filter(Boolean))];
  const categories = [...new Set(appliances.map(appliance => appliance.category).filter(Boolean))];
  const designStyles = [...new Set(appliances.map(appliance => appliance.design_style).filter(Boolean))];

  // Enhanced refresh function that reloads all appliances
  const handleRefreshAllAppliances = async () => {
    console.log('Refreshing all appliances data...');
    await fetchAppliances();
    await fetchDesignInsights();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading luxury appliances...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={fetchAppliances}
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
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Luxe Appliances</h1>
            <p className="text-lg text-gray-600">Design insights and renovation trends for luxury kitchen appliances</p>
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
                  Search Appliances
                </label>
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search by name, brand, or description..."
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
                  <option value="rating">Overall Rating (Highest First)</option>
                  <option value="design_rating">Design Rating (Highest First)</option>
                  <option value="price">Price (Highest First)</option>
                  <option value="brand">Brand (A-Z)</option>
                  <option value="name">Name (A-Z)</option>
                </select>
              </div>

              {/* Brand Filter */}
              <div className="mb-6">
                <label htmlFor="brand" className="block text-sm font-medium text-gray-700 mb-2">
                  Brand
                </label>
                <select
                  id="brand"
                  value={filterBrand}
                  onChange={(e) => setFilterBrand(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Brands</option>
                  {brands.map(brand => (
                    <option key={brand} value={brand}>{brand}</option>
                  ))}
                </select>
              </div>

              {/* Category Filter */}
              <div className="mb-6">
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  id="category"
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Categories</option>
                  {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              {/* Design Style Filter */}
              <div className="mb-6">
                <label htmlFor="designStyle" className="block text-sm font-medium text-gray-700 mb-2">
                  Design Style
                </label>
                <select
                  id="designStyle"
                  value={filterDesignStyle}
                  onChange={(e) => setFilterDesignStyle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Styles</option>
                  {designStyles.map(style => (
                    <option key={style} value={style}>{style}</option>
                  ))}
                </select>
              </div>

              {/* Results Count */}
              <div className="pt-4 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  Showing {filteredAndSortedAppliances.length} of {appliances.length} appliances
                </p>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Design Insights Summary */}
            {designInsights && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Design Insights</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Top Design Trends</h3>
                    <div className="space-y-2">
                      {Object.entries(designInsights.design_trends || {}).slice(0, 5).map(([trend, count]) => (
                        <div key={trend} className="flex justify-between text-sm">
                          <span className="text-gray-600">{trend}</span>
                          <span className="font-medium text-gray-900">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900 mb-2">Competitor Mentions</h3>
                    <div className="space-y-2">
                      {Object.entries(designInsights.competitor_mentions || {}).slice(0, 5).map(([competitor, count]) => (
                        <div key={competitor} className="flex justify-between text-sm">
                          <span className="text-gray-600">{competitor}</span>
                          <span className="font-medium text-gray-900">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Appliances Grid */}
            {filteredAndSortedAppliances.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg mb-2">No appliances found</div>
                <p className="text-gray-400">Try adjusting your search or filters</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredAndSortedAppliances.map(appliance => (
                  <LuxeApplianceCard key={appliance.id} appliance={appliance} onRefresh={handleRefreshAllAppliances} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LuxeApplianceList; 