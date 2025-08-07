import React, { useState, useEffect } from 'react';
import LuxeApplianceCard from '../components/LuxeApplianceCard';
import FilterBar from '../components/FilterBar';
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
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    fetchAppliances();
    fetchDesignInsights();
  }, []);

  // Handle scroll events for responsive header
  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
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

  // Define filter options for the FilterBar component
  const sortOptions = [
    { value: 'rating', label: 'Overall Rating (Highest First)' },
    { value: 'design_rating', label: 'Design Rating (Highest First)' },
    { value: 'price', label: 'Price (Highest First)' },
    { value: 'brand', label: 'Brand (A-Z)' },
    { value: 'name', label: 'Name (A-Z)' }
  ];

  const filters = [
    {
      label: 'Brand',
      value: filterBrand,
      onChange: setFilterBrand,
      options: brands,
      allLabel: 'All Brands'
    },
    {
      label: 'Category',
      value: filterCategory,
      onChange: setFilterCategory,
      options: categories,
      allLabel: 'All Categories'
    },
    {
      label: 'Design Style',
      value: filterDesignStyle,
      onChange: setFilterDesignStyle,
      options: designStyles,
      allLabel: 'All Styles'
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
                className="inline-flex items-center justify-center rounded-xl mb-4 bg-gradient-to-br from-green-500 to-teal-600 text-white shadow-lg transition-all duration-300"
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h1 
                className="font-bold text-gray-800 dark:text-white mb-2 transition-all duration-300"
                style={{ 
                  fontSize: `${titleSize}px`,
                  marginBottom: `${Math.max(3, 6 - scrollY / 40)}px` // Reduced from 4-8 to 3-6
                }}
              >
                Luxury Appliances
              </h1>
              <p 
                className="text-gray-500 dark:text-gray-400 transition-all duration-300"
                style={{ 
                  fontSize: `${subtitleSize}px`,
                  opacity: subtitleOpacity,
                  transform: `translateY(${(1 - subtitleOpacity) * -10}px)`
                }}
              >
                Design insights and renovation trends for premium kitchen appliances
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
        resultsCount={filteredAndSortedAppliances.length}
        totalCount={appliances.length}
        placeholder="Search by name, brand, or description..."
      />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Design Insights Summary */}
        {designInsights && (
          <div className="bg-white dark:bg-dark-card rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Design Insights</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-gray-800 dark:text-white mb-2">Top Design Trends</h3>
                <div className="space-y-2">
                  {Object.entries(designInsights.design_trends || {}).slice(0, 5).map(([trend, count]) => (
                    <div key={trend} className="flex justify-between text-sm">
                      <span className="text-gray-500 dark:text-gray-400">{trend}</span>
                      <span className="font-medium text-gray-800 dark:text-white">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="font-medium text-gray-800 dark:text-white mb-2">Competitor Mentions</h3>
                <div className="space-y-2">
                  {Object.entries(designInsights.competitor_mentions || {}).slice(0, 5).map(([competitor, count]) => (
                    <div key={competitor} className="flex justify-between text-sm">
                      <span className="text-gray-500 dark:text-gray-400">{competitor}</span>
                      <span className="font-medium text-gray-800 dark:text-white">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Appliances Grid */}
        {filteredAndSortedAppliances.length === 0 ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div className="text-gray-500 dark:text-gray-400 text-lg mb-2">No appliances found</div>
            <p className="text-gray-400 dark:text-gray-500">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-8">
            {filteredAndSortedAppliances.map(appliance => (
              <LuxeApplianceCard key={appliance.id} appliance={appliance} onRefresh={handleRefreshAllAppliances} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LuxeApplianceList; 