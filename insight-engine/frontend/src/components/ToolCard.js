import React, { useState } from 'react';
import apiService from '../services/api';

const ToolCard = ({ tool, onRefresh }) => {
  const { name, short_description, website, pricing_model, primary_use_case, aggregated_review } = tool;
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Generate star rating display
  const renderStars = (rating) => {
    if (!rating) return <span className="text-gray-400">No rating</span>;
    
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <svg key={`full-${i}`} className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }
    
    // Half star
    if (hasHalfStar) {
      stars.push(
        <svg key="half" className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
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
        <svg key={`empty-${i}`} className="w-4 h-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }
    
    return <div className="flex">{stars}</div>;
  };

  const handleRefreshReviews = async () => {
    setIsRefreshing(true);
    try {
      await apiService.refreshReviews(tool.id);
      if (onRefresh) {
        onRefresh();
      }
    } catch (error) {
      console.error('Error refreshing reviews:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">{name}</h3>
            {website && (
              <a
                href={website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary-600 hover:text-primary-700 underline"
              >
                Visit Website
              </a>
            )}
          </div>
          
          {/* Rating */}
          <div className="flex items-center space-x-2">
            {aggregated_review && (
              <div className="text-right">
                <div className="flex items-center space-x-1">
                  {renderStars(aggregated_review.overall_rating)}
                  <span className="text-sm font-medium text-gray-900">
                    {aggregated_review.overall_rating?.toFixed(1)}
                  </span>
                </div>
                <span className="text-xs text-gray-500">Overall Rating</span>
              </div>
            )}
          </div>
        </div>

        {/* Description */}
        {short_description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {short_description}
          </p>
        )}

        {/* Sentiment Summaries */}
        {aggregated_review && (
          <div className="mb-4 space-y-2">
            {aggregated_review.positive_sentiment_summary && (
              <div className="text-xs">
                <span className="font-medium text-green-600">👍 Positive:</span>
                <span className="text-gray-600 ml-1">{aggregated_review.positive_sentiment_summary}</span>
              </div>
            )}
            {aggregated_review.negative_sentiment_summary && (
              <div className="text-xs">
                <span className="font-medium text-red-600">👎 Negative:</span>
                <span className="text-gray-600 ml-1">{aggregated_review.negative_sentiment_summary}</span>
              </div>
            )}
          </div>
        )}

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {pricing_model && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {pricing_model}
            </span>
          )}
          {primary_use_case && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              {primary_use_case}
            </span>
          )}
        </div>

        {/* Refresh Reviews Button */}
        <button
          onClick={handleRefreshReviews}
          disabled={isRefreshing}
          className={`w-full px-3 py-2 text-sm font-medium rounded-md transition-colors ${
            isRefreshing
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-primary-50 text-primary-700 hover:bg-primary-100'
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