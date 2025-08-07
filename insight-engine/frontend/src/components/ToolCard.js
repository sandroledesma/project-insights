import React, { useState } from 'react';
import LogoDisplay from './LogoDisplay';
import apiService from '../services/api';

const ToolCard = ({ tool, onRefresh }) => {
  const { name, short_description, website, pricing_model, primary_use_case, aggregated_review } = tool;
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Generate star rating display
  const renderStars = (rating) => {
    if (!rating) return <span className="text-gray-400 text-sm">No rating</span>;
    
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <svg key={`full-${i}`} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }
    
    // Half star
    if (hasHalfStar) {
      stars.push(
        <svg key="half" className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <defs>
            <linearGradient id="half-star">
              <stop offset="50%" stopColor="currentColor" />
              <stop offset="50%" stopColor="#e5e7eb" />
            </linearGradient>
          </defs>
          <path fill="url(#half-star)" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }
    
    // Empty stars
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <svg key={`empty-${i}`} className="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }
    
    return <div className="flex">{stars}</div>;
  };

  const handleRefreshReviews = async () => {
    console.log('Starting refresh for tool:', tool.id, tool.name);
    setIsRefreshing(true);
    try {
      console.log('Calling API...');
      const result = await apiService.refreshReviews(tool.id);
      console.log('API result:', result);
      
      if (onRefresh) {
        console.log('Calling onRefresh callback...');
        onRefresh();
      }
      
      // Show success message
      alert(`Reviews refreshed! Found ${result.total_reviews} reviews in ${result.search_time}s`);
      
    } catch (error) {
      console.error('Error refreshing reviews:', error);
      alert(`Error refreshing reviews: ${error.message}`);
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="bg-white dark:bg-dark-card rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg dark:hover:shadow-2xl transition-all duration-300 overflow-hidden group">
      {/* Header with logo, title, and rating */}
      <div className="p-8">
        <div className="flex items-start space-x-6">
          {/* Logo */}
          <div className="flex-shrink-0">
            <LogoDisplay 
              name={name}
              website={website}
              size="xl"
              className="group-hover:scale-105 transition-transform duration-200"
            />
          </div>
          
          {/* Content */}
          <div className="flex-1 min-w-0">
            {/* Title (clickable to website) */}
            <div className="mb-4">
              {website ? (
                <a
                  href={website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block group/title"
                >
                  <h3 className="text-2xl font-bold text-gray-800 dark:text-white group-hover/title:text-accent-green transition-colors duration-200 leading-tight">
                    {name}
                  </h3>
                </a>
              ) : (
                <h3 className="text-2xl font-bold text-gray-800 dark:text-white leading-tight">
                  {name}
                </h3>
              )}
            </div>

            {/* Description */}
            {short_description && (
              <p className="text-gray-600 dark:text-gray-300 text-base leading-relaxed mb-6">
                {short_description}
              </p>
            )}

            {/* Rating - separate section */}
            {aggregated_review && (
              <div className="flex items-center space-x-3 mb-6">
                <div className="flex items-center space-x-2">
                  {renderStars(aggregated_review.overall_rating)}
                </div>
                <div className="flex items-baseline space-x-1">
                  <span className="text-2xl font-bold text-gray-800 dark:text-white">
                    {aggregated_review.overall_rating?.toFixed(1)}
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">/5</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>


      {/* Tags */}
      <div className="px-8 py-5 bg-gray-50 dark:bg-gray-800/30 border-t border-gray-100 dark:border-gray-700">
        <div className="flex flex-wrap gap-3">
          {pricing_model && (
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-accent-green/10 text-accent-green border border-accent-green/20">
              {pricing_model}
            </span>
          )}
          {primary_use_case && (
            <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700">
              {primary_use_case}
            </span>
          )}
        </div>
      </div>

      {/* Sentiment Summaries */}
      {aggregated_review && (
        <div className="px-8 py-6 space-y-6 border-t border-gray-100 dark:border-gray-700">
          {aggregated_review.positive_sentiment_summary && (
            <div>
              <div className="flex items-center mb-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                <span className="font-semibold text-green-700 dark:text-green-400 text-base">
                  What Users Love
                </span>
              </div>
              <p className="text-gray-600 dark:text-gray-300 text-base leading-relaxed pl-5">
                {aggregated_review.positive_sentiment_summary}
              </p>
            </div>
          )}
          {aggregated_review.negative_sentiment_summary && (
            <div>
              <div className="flex items-center mb-3">
                <div className="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                <span className="font-semibold text-orange-700 dark:text-orange-400 text-base">
                  Common Concerns
                </span>
              </div>
              <p className="text-gray-600 dark:text-gray-300 text-base leading-relaxed pl-5">
                {aggregated_review.negative_sentiment_summary}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Refresh Button */}
      <div className="p-8 border-t border-gray-100 dark:border-gray-700">
        <button
          onClick={handleRefreshReviews}
          disabled={isRefreshing}
          className={`w-full px-6 py-3 text-base font-medium rounded-xl transition-all duration-200 ${
            isRefreshing
              ? 'bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
              : 'bg-accent-green/10 text-accent-green hover:bg-accent-green/20 border border-accent-green/20 dark:border-accent-green/30 hover:shadow-md'
          }`}
        >
          {isRefreshing ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Refreshing Reviews...
            </span>
          ) : (
            <span className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh Reddit Reviews
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

export default ToolCard; 