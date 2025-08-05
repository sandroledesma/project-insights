import React, { useState } from 'react';
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
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 overflow-hidden group">
      {/* Header with rating */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
              {name}
            </h3>
            {website && (
              <a
                href={website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:text-blue-700 underline inline-flex items-center"
              >
                Visit Website
                <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            )}
          </div>
          
          {/* Rating */}
          <div className="text-right">
            {aggregated_review ? (
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-1">
                  {renderStars(aggregated_review.overall_rating)}
                  <span className="text-lg font-bold text-gray-900 ml-1">
                    {aggregated_review.overall_rating?.toFixed(1)}
                  </span>
                </div>
                <span className="text-xs text-gray-500">/5</span>
              </div>
            ) : (
              <span className="text-gray-400 text-sm">No rating</span>
            )}
          </div>
        </div>

        {/* Description */}
        {short_description && (
          <p className="text-gray-600 text-sm leading-relaxed">
            {short_description}
          </p>
        )}
      </div>

      {/* Tags */}
      <div className="px-6 py-3 bg-gray-50">
        <div className="flex flex-wrap gap-2">
          {pricing_model && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {pricing_model}
            </span>
          )}
          {primary_use_case && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
              {primary_use_case}
            </span>
          )}
        </div>
      </div>

      {/* Sentiment Summaries */}
      {aggregated_review && (
        <div className="px-6 py-4 space-y-3">
          {aggregated_review.positive_sentiment_summary && (
            <div className="text-sm">
              <span className="font-medium text-green-600 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Positive:
              </span>
              <p className="text-gray-600 mt-1 text-xs leading-relaxed">
                {aggregated_review.positive_sentiment_summary}
              </p>
            </div>
          )}
          {aggregated_review.negative_sentiment_summary && (
            <div className="text-sm">
              <span className="font-medium text-red-600 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                Negative:
              </span>
              <p className="text-gray-600 mt-1 text-xs leading-relaxed">
                {aggregated_review.negative_sentiment_summary}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Refresh Button */}
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
        <button
          onClick={handleRefreshReviews}
          disabled={isRefreshing}
          className={`w-full px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            isRefreshing
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200'
          }`}
        >
          {isRefreshing ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Refreshing...
            </span>
          ) : (
            <span className="flex items-center justify-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
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